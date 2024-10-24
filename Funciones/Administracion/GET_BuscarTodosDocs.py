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
from Funciones.Servicios.Autenticacion import AutenticacionUsuario

GET_BuscarTodosDocs = Blueprint('GET_BuscarTodosDocs', __name__)

@GET_BuscarTodosDocs.route('/BuscarTodosDocumentos', methods=['GET'])
def BuscarDocumentos():
    try:

        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['admin'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        coleccion_doc = mongo.db['documentos']
        coleccion_usr = mongo.db['Usuarios']
        coleccion_cal = mongo.db['calificaciones']
        coleccion_uni = mongo.db['universidades']
        coleccion_mat = mongo.db['materias'] 

        documentos = list(coleccion_doc.find())
        lista_documentos = []


        for doc in documentos:

            materia = coleccion_mat.find_one({'_id': doc['materia_id']})
            usuario = coleccion_usr.find_one({'_id': doc['usuario_id']})
            universidad = coleccion_uni.find_one({'_id': usuario['universidad_id']})

            total_com = len(list(coleccion_cal.find({'documento': doc['_id']})))

            lista_documentos.append({
                'id': str(doc['_id']),
                "titulo": doc['titulo'],
                'materia': materia['nombre'],
                'tipo_documento': doc['tipo_documento'],
                'usuario': usuario['nombre_completo'],
                'universidad': universidad['nombre'],
                'fecha_subida': doc['fecha_subida'].strftime("%d/%m/%Y"),
                'fecha_modificacion': doc['fecha_modificacion'].strftime("%d/%m/%Y"),
                'calificacion_promedio': doc['calificacion_promedio'],
                'numero_calificaciones': total_com,
                'aprobado': doc['aprobado'],
                'numero_reportes': doc['numero_reportes']
            })

        return jsonify(lista_documentos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500