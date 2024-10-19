import os
import sys
import json
from datetime import datetime
from bson.objectid import ObjectId
from statistics import mean

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

POST_AgregarCal = Blueprint('POST_AgregarCal', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (id usuario, id documento, calificacion)
@POST_AgregarCal.route('/AgregarCalificacion', methods=['POST'])
def AgregarCalificacion():
    try:

        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        usuario_id = ObjectId(datos_json['usr_id'])
        documento_id = ObjectId(datos_json['doc_id'])
        calificacion = int(datos_json['calificacion'])
        #comentario = int(datos_json['comentario'])
        fecha = datetime.now()

        coleccion_usr = mongo.db['Usuarios']
        coleccion_doc = mongo.db['documentos']

        exist_usr = coleccion_usr.find_one({'_id': usuario_id})
        if not exist_usr:
            return jsonify({'error': 'No existe el usuario'}), 400 

        exist_doc = coleccion_doc.find_one({'_id': documento_id})
        if not exist_doc:
            return jsonify({'error': 'No existe el documento'}), 400 
        
        if calificacion <= 0 and calificacion > 5:
            return jsonify({'error': 'Calificacion por fuera del rango'}), 400

        documento = {
            "usuario": usuario_id, 
            "documento": documento_id,
            #"comentario": comentario,
            "calificacion": calificacion,
            "fecha": fecha
        }

        
        coleccion_doc = mongo.db['calificaciones']
        lista_calificaciones = list(coleccion_doc.find())
        lista_promedio = []

        for calif in lista_calificaciones:
            lista_promedio.append(calif['calificacion'])

        lista_promedio.append(calificacion)
        nueva_calificacion = round(mean(lista_promedio), 1)

        documento_actualizado = {
            "calificacion_promedio": nueva_calificacion
        }

        resultado_1 = mongo.db.calificaciones.insert_one(documento)
        resultado_2 = mongo.db.documentos.update_one({"_id": documento_id}, {"$set": documento_actualizado})

        return jsonify({"ok": "se creo el comentario correctamente"}), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500 