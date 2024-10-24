import os
import sys
import json
from bson.objectid import ObjectId

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )

from flask import Blueprint, request, jsonify
from Funciones.Servicios.Autenticacion import AutenticacionUsuario

POST_ReportarDoc = Blueprint('POST_ReportarDoc', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (id usuario, id documento)
@POST_ReportarDoc.route('/ReportarDocumento', methods=['POST'])
def ReportarDocumento():
    try:

        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['usuario'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        #usuario_id = ObjectId(datos_json['usr_id'])
        usuario_id = ObjectId(usuario['_id'])
        documento_id = ObjectId(datos_json['doc_id'])

        coleccion_usr = mongo.db['Usuarios']
        coleccion_doc = mongo.db['documentos']

        exist_usr = coleccion_usr.find_one({'_id': usuario_id})
        if not exist_usr:
            return jsonify({'error': 'No existe el usuario'}), 400 

        exist_doc = coleccion_doc.find_one({'_id': documento_id})
        if not exist_doc:
            return jsonify({'error': 'No existe el documento'}), 400 

        documento = {
            "numero_reportes": exist_doc['numero_reportes'] + 1, 
        }

        resultado = mongo.db.documentos.update_one({"_id": documento_id}, {"$set": documento})

        return jsonify({"ok": "se reporto el documento, el administrador luego lo vera"}), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500 