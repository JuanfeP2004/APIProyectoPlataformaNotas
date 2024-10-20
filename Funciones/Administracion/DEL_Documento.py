import os
import sys
import json
from bson.objectid import ObjectId

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

DEL_Documento = Blueprint('DEL_Documento', __name__)

# (id)
@DEL_Documento.route('/BorrarDocumento', methods=['DELETE'])
def BorrarDocumento():
    try:
        
        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        documento_id = ObjectId(datos_json['id'])

        documentos = mongo.db['documentos']
        calificaciones = mongo.db['calificaciones']

        documento = documentos.find_one({'_id': documento_id})
        if not documento:
            return jsonify({'error': 'No existe ese documento'}), 400 

        cliente = storage.get_blob_client(container=contenedor, blob=documento['archivo'])

        resultado_1 = calificaciones.delete_many({"documento": documento_id})
        resultado_2 = documentos.delete_one({"_id": documento_id})
        cliente.delete_blob()

        return jsonify({"ok": "Se ha borrado el documento correctamente"}), 200
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500 