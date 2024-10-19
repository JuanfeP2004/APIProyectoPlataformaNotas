import os
import sys
import uuid
import json
from datetime import datetime
from bson.objectid import ObjectId

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

POST_SubirDoc = Blueprint('POST_SubirDoc', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (nombre, tipo, materia, universidad)
@POST_SubirDoc.route('/SubirDocumento', methods=['POST'])
def SubirDocumento():
    try:
        from app import mongo

        if "file" not in request.files:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400
        if "json" not in request.form:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'No se proporcionó un json'}), 400
    
        archivo = request.files["file"]
        datos_json = json.loads(metadatos)

        titulo = datos_json['titulo']
        usuario_id = ObjectId(datos_json['usr_id'])
        tipo = str.upper(datos_json['tipo'])
        materia = str.upper(datos_json['materia'])
        fecha = datetime.now()


        coleccion_usr = mongo.db['Usuarios']
        materias = mongo.db['materias']

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


        ubicacion = str(uuid.uuid4())
        #ubicacion = unique_id + '_' + archivo.filename

        cliente = storage.get_blob_client(container=contenedor, blob=ubicacion)
        cliente.upload_blob(archivo)

        documento = {
            "titulo": titulo,
            "usuario_id": usuario_id, 
            "materia_id": val_mat['_id'],
            "tipo_documento": tipo,
            "fecha_subida": fecha,
            "fecha_modificacion": fecha,
            "archivo": ubicacion,
            "numero_descargas": 0,
            "calificacion_promedio": 0,
            "aprobado": False
        }

        resultado = mongo.db.documentos.insert_one(documento)

        return jsonify({"ok": f"Usuario agregado con id: {resultado.inserted_id}"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    

