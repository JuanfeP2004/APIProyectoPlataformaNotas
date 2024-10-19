import os
import sys
import uuid
import json

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor
from app import mongo

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

DEL_Documento = Blueprint('DEL_Documento', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (nombre, tipo, materia, universidad)
@DEL_Documento.route('/BorrarDocumento', methods=['DELETE'])
def BorrarDocumento():
    try:
        '''
        metadatos = request.form.get('json')

        if not metadatos:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        datos = request.form['json']
        datos_json = json.loads(datos)

        id = datos_json['id']

        resultado = mongo.db.comentarios.delete_one({"_id": ObjectId(id)})

        if resultado.deleted_count > 0:
            return f"Usuario con id {id} eliminado correctamente."
        else:
            return jsonify({"error": 'Usuario no encontrado'}), 400
        '''
    except Exception as e:
        return jsonify({"error": str(e)}), 500 