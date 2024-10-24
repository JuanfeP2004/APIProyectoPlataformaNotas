import os
import sys
import json
from bson.objectid import ObjectId
from datetime import datetime

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor
from Servicios.Autenticacion import AutenticacionUsuario

from flask import Blueprint, request, jsonify

PUT_EditarDoc = Blueprint('PUT_EditarDoc', __name__)

@PUT_EditarDoc.route('/EditarDocumento', methods=['PUT'])
def EditarDocumento():
    try:
        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['usuario','admin'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        #if "file" not in request.files:
        #    return jsonify({'error': 'No se proporcionó un archivo'}), 400
        if "json" not in request.form:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'No se proporcionó un json'}), 400
    
        datos_json = json.loads(metadatos)

        id = ObjectId(datos_json['id'])
        titulo = datos_json['titulo']
        #usuario_id = ObjectId(datos_json['usr_id'])
        usuario_id = ObjectId(usuario['_id'])
        tipo = str.upper(datos_json['tipo'])
        materia = str.upper(datos_json['materia'])
        fecha = datetime.now()


        coleccion_usr = mongo.db['Usuarios']
        coleccion_doc = mongo.db['documentos']
        materias = mongo.db['materias']

        existe_documento = coleccion_doc.find_one({'_id': id})

        if not existe_documento:
            return jsonify({'error': 'No existe ese documento'}), 400

        existe_usuario = coleccion_usr.find_one({"_id": usuario_id})
        val_mat = materias.find_one({"nombre": materia})

        if titulo in (None, ''):
            return jsonify({'error': 'El titulo no puede estar en blanco o vacio'}), 400
        if tipo in (None, ''):
            return jsonify({'error': 'El tipo de documento no puede estar en blanco o vacio'}), 400
        if not existe_usuario:
            return jsonify({'error': 'No existe ese usuario'}), 400
        elif not val_mat:
            return jsonify({'error': 'No existe esa materia'}), 400

        if "file" in request.files:
            archivo = request.files["file"]
            cliente = storage.get_blob_client(container=contenedor, blob=existe_documento['archivo'])
       
            cliente.upload_blob(archivo, overwrite=True)

        documento = {
            "titulo": titulo,
            "materia_id": val_mat['_id'],
            "tipo_documento": tipo,
            "fecha_modificacion": fecha,
        }

        resultado = mongo.db.documentos.update_one({"_id": id}, {"$set": documento})

        return jsonify({"ok": 'Se actualizo el documento correctamente'}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500