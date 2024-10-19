import os
import sys
import io
import json
from bson.objectid import ObjectId
from datetime import datetime

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify

GET_BuscarMisDocs = Blueprint('GET_BuscarMisDocs', __name__)

@GET_BuscarMisDocs.route('/BuscarMisDocumentos', methods=['GET'])
def BuscarMisDocumentos():
    try:

        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        usuario_id = ObjectId(datos_json['id'])

        coleccion_doc = mongo.db['documentos']
        coleccion_usr = mongo.db['Usuarios']
        coleccion_cal = mongo.db['calificaciones']
        coleccion_uni = mongo.db['universidades']
        coleccion_mat = mongo.db['materias']

        usuario = coleccion_usr.find_one({'_id': usuario_id})
        if not usuario:
            return jsonify({'error': 'No existe el usuario'}), 400 

        documentos = list(coleccion_doc.find({'usuario_id': usuario_id}))
        lista_documentos = []


        for doc in documentos:

            materia = coleccion_mat.find_one({'_id': doc['materia_id']})
            #usuario = coleccion_usr.find_one({'_id': doc['usuario_id']})
            universidad = coleccion_uni.find_one({'_id': usuario['universidad_id']})

            total_com = len(list(coleccion_cal.find({'documento': doc['_id']})))

            lista_documentos.append({
                'id': str(doc['_id']),
                "titulo": doc['titulo'],
                'materia': materia['nombre'],
                'tipo_documento': doc['tipo_documento'],
                'fecha_subida': doc['fecha_subida'].strftime("%d/%m/%Y"),
                'fecha_modificacion': doc['fecha_modificacion'].strftime("%d/%m/%Y"),
                'calificacion_promedio': doc['calificacion_promedio'],
                'numero_calificaciones': total_com,
                'aprobado': doc['aprobado']
            })

        return jsonify(lista_documentos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500