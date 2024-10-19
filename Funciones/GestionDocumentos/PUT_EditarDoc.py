import os
import sys
import uuid
import json

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

PUT_EditarDoc = Blueprint('PUT_EditarDoc', __name__)

@PUT_EditarDoc.route('/EditarDocumento', methods=['PUT'])
def EditarDocumento():
    try:
        if "file" not in request.files:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400

        metadatos = request.form.get('json')

        if not metadatos:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        datos = request.form['json']      
        archivo = request.files["file"]
        datos_json = json.loads(datos)

        nombre = datos_json['nombre']
        tipo = datos_json['tipo']
        materia = datos_json['materia']
        universidad = datos_json['universidad']

        unique_id = str(uuid.uuid4())
        ubicacion = unique_id + '_' + archivo.filename

        cliente = storage.get_blob_client(container=contenedor, blob=ubicacion)
        cliente.upload_blob(archivo)

        return 'Se subio el archivo correctamente'
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500