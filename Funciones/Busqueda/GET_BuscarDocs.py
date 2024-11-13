import os
import sys
import io
import json
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import cross_origin

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor

from flask import Blueprint, request, jsonify

GET_BuscarDocs = Blueprint('GET_BuscarDocs', __name__)

@GET_BuscarDocs.route('/BuscarDocumentos', methods=['GET'])
@cross_origin()
def BuscarDocumentos():
    try:

        from app import mongo

        limite = 3
        lista_limite = []

        coleccion_doc = mongo.db['documentos']
        coleccion_usr = mongo.db['Usuarios']
        coleccion_cal = mongo.db['calificaciones']
        coleccion_uni = mongo.db['universidades']
        coleccion_mat = mongo.db['materias']

        documentos = list(coleccion_doc.find({"aprobado":True}))
        lista_documentos = []


        # Hacer cosas aca
        if not len(documentos) < limite:
            for i in range(limite):
                lista_limite.append(lista_documentos[i])

            for doc in lista_limite:

                materia = coleccion_mat.find_one({'_id': doc['materia_id']})
                usuario = coleccion_usr.find_one({'_id': doc['usuario_id']})
                universidad = coleccion_uni.find_one({'_id': usuario['universidad_id']})

                total_com = len(list(coleccion_cal.find({'_id': doc['_id']})))

                lista_documentos.append({
                    'id': str(doc['_id']),
                    "titulo": doc['titulo'],
                    'materia': materia['nombre'],
                    'universidad': universidad['nombre'],
                    'tipo': doc['tipo'],
                    'usuario': usuario['nombre'],
                    'fecha_modificacion': doc['fecha_modificacion'].strftime("%d/%m/%Y"),
                    'calificacion_promedio': doc['calificacion_promedio'],
                    'numero_calificaciones': total_com
                })

        else:

            for doc in documentos:

                materia = coleccion_mat.find_one({'_id': doc['materia_id']})
                usuario = coleccion_usr.find_one({'_id': doc['usuario_id']})
                universidad = coleccion_uni.find_one({'_id': usuario['universidad_id']})

                total_com = len(list(coleccion_cal.find({'documento': doc['_id']})))

                lista_documentos.append({
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

            return jsonify(lista_documentos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500