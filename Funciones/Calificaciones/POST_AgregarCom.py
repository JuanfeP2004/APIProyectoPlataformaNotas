import os
import sys
import uuid
import json
from datetime import datetime

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from app import mongo

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

POST_AgregarCom = Blueprint('POST_AgregarCom', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (nombre, tipo, materia, universidad)
@POST_AgregarCom.route('/AgregarComentario', methods=['POST'])
def AgregarComentario():
    try:

        if "json" not in request.files:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400

        metadatos = request.form.get('json')

        if not metadatos:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        datos = request.form['json']      

        datos_json = json.loads(datos)

        usuario_id = datos_json['usr_id']
        documento_id = datos_json['doc_id']
        calificacion = int(datos_json['calificacion'])
        fecha = datetime.now()

        documento = {
            "usuario": usuario_id, 
            "documento": documento_id,
            "calificacion": calificacion,
            "fecha": fecha
        }

        resultado = mongo.db.Calificaciones.insert_one(documento)

        return jsonify({"ok": "se creo el comentario correctamente"}), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500 