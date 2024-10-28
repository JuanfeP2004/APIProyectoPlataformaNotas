import os
import sys
import json
from bson.objectid import ObjectId
from flask_cors import cross_origin

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor
from Servicios.Autenticacion import AutenticacionUsuario

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

DEL_BorrarUsuario = Blueprint('DEL_BorrarUsuario', __name__)

# Esta funcion borra un usuario con todos sus documentos subidos
# (id)
@DEL_BorrarUsuario.route('/BorrarUsuario', methods=['DELETE'])
@cross_origin()
def BorrarUsuario():
    try:
        
        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['admin'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        usuario_id = ObjectId(datos_json['id'])

        usuarios = mongo.db['Usuarios']
        documentos = mongo.db['documentos']
        calificaciones = mongo.db['calificaciones']

        usuario = usuarios.find_one({'_id': usuario_id})
        if not usuario:
            return jsonify({'error': 'No existe ese usuario'}), 400 

        documentos_usr = list(documentos.find({'usuario_id': usuario_id}))


        #usuario_borrado_doc = {
        #    "usuario_id": "Eliminado"
        #}
        #usuario_borrado_cal = {
        #    "usuario": "Eliminado"
        #}
        #calificaciones.update_many({"usuario": usuario_id}, {"$set":usuario_borrado_cal})

        for doc in documentos_usr:

            cliente = storage.get_blob_client(container=contenedor, blob=doc['archivo'])

            resultado_1 = calificaciones.delete_many({"documento": doc['_id']})
            resultado_2 = documentos.delete_one({"_id": doc['_id']})
            cliente.delete_blob()

        resultado = usuarios.delete_one({'_id': usuario_id})

        return jsonify({"ok": "Se ha borrado el usuario correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 