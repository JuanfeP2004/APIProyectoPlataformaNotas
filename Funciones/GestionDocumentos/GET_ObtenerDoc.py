import os
import sys
import io
import json
from bson.objectid import ObjectId

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify, send_file

GET_ObtenerDoc = Blueprint('GET_ObtenerDoc', __name__)

@GET_ObtenerDoc.route('/ObtenerDocumento', methods=['GET'])
def ObtenerDocumento():
    try:

        from app import mongo

        if "json" not in request.form:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400    

        datos_json = json.loads(metadatos)    

        id = ObjectId(datos_json['id'])

        coleccion_doc = mongo.db['documentos']

        existe_doc = coleccion_doc.find_one({'_id': id})

        if not existe_doc:
            return jsonify({'error': 'No existe ese documento'}), 400

        cliente = storage.get_blob_client(container=contenedor, blob=existe_doc['archivo'])
        archivo = cliente.download_blob().readall()

        return send_file(io.BytesIO(archivo), download_name=existe_doc['archivo'], as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500