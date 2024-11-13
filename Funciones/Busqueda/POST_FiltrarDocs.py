import os
import sys
import io
import json
from bson.objectid import ObjectId
from datetime import datetime
import traceback
from flask_cors import cross_origin

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify

GET_FiltrarDocs = Blueprint('GET_FiltrarDocs', __name__)

@GET_FiltrarDocs.route('/FiltrarDocumentos', methods=['POST'])
@cross_origin()
def FiltrarDocumentos():
    try:

        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        patron = datos_json['nombre']
        str_universidad = datos_json['universidad']
        str_materia = datos_json['asignatura']
        tipo = datos_json['tipo']

        coleccion_doc = mongo.db['documentos']
        coleccion_usr = mongo.db['Usuarios']
        coleccion_cal = mongo.db['calificaciones']
        coleccion_uni = mongo.db['universidades']
        coleccion_mat = mongo.db['materias']

        materia = coleccion_mat.find_one({'nombre': str.upper(str_materia)})
        if not materia and str_materia != '':
            return jsonify({'error': 'La materia no existe'}), 400  

        universidad = coleccion_uni.find_one({'nombre': str_universidad})
        if not universidad and str_universidad != '':
            return jsonify({'error': 'La universidad no existe'}), 400
              

        documentos = list(coleccion_doc.find({"aprobado":True}))

        lista_documentos = []
        lista_retorno = []

        for documento in documentos:

            if(patron != ''):
                if (patron not in documento['titulo']):
                    continue

            if(tipo != ''):
                if (str.upper(tipo) != documento['tipo_documento']):
                    continue
            
            if(str_materia != ''):
                if (str(materia['_id']) != str(documento['materia_id'])):
                    continue

            if(str_universidad != ''):
                usuario = coleccion_usr.find_one({'universidad_id': universidad['_id']})
                if not usuario:
                    continue

            lista_documentos.append(documento)


        for doc in lista_documentos:
            materia = coleccion_mat.find_one({'_id': doc['materia_id']})
            usuario = coleccion_usr.find_one({'_id': doc['usuario_id']})
            universidad = coleccion_uni.find_one({'_id': usuario['universidad_id']})

            total_com = len(list(coleccion_cal.find({'documento': doc['_id']})))

            lista_retorno.append({
                'id': str(doc['_id']),
                "titulo": doc['titulo'],
                'materia': materia['nombre'],
                'universidad': universidad['nombre'],
                'tipo_documento': doc['tipo_documento'],
                'usuario': usuario['nombre_completo'],
                'fecha_modificacion': doc['fecha_modificacion'].strftime("%d/%m/%Y"),
                'calificacion_promedio': doc['calificacion_promedio'],
                'numero_calificaciones': total_com
            })

        return jsonify(lista_retorno), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500