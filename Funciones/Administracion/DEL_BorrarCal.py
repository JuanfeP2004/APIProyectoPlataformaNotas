import os
import sys
import traceback
import json
from bson.objectid import ObjectId
from statistics import mean
from flask_cors import cross_origin

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )

from flask import Blueprint, request, jsonify
from Servicios.Autenticacion import AutenticacionUsuario

DEL_Comentario = Blueprint('DEL_Comentario', __name__)

# Esta funcion recibe un DEL
# (id)
@DEL_Comentario.route('/BorrarCalificacion', methods=['DELETE'])
@cross_origin()
def BorrarCalificacion():
    try:

        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['admin'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400   

        datos_json = json.loads(metadatos)

        calificacion_id = ObjectId(datos_json['id'])
        
        comentarios = mongo.db['calificaciones']
        documentos = mongo.db['documentos']

        calificacion = comentarios.find_one({'_id': calificacion_id})
        if not calificacion:
            return jsonify({'error': 'No existe esa calificacion'}), 400
        
        documento_cal = documentos.find_one({'_id': calificacion['documento']})

        lista_calificaciones = list(comentarios.find())
        lista_promedio = []

        for calif in lista_calificaciones:
            if(calif['_id'] == calificacion_id):
                continue
            lista_promedio.append(calif['calificacion'])

        nueva_calificacion = round(mean(lista_promedio), 1)

        documento_actualizado = {
            "calificacion_promedio": nueva_calificacion
        }

        resultado_2 = mongo.db.documentos.update_one({"_id": documento_cal['_id']}, {"$set": documento_actualizado})
        resultado_1 = mongo.db.calificaciones.delete_one({"_id": calificacion_id})

        return jsonify({"ok": 'La calificacion se borro correctamente'}), 200

    except Exception as e:
        return jsonify({"error": traceback.format_exc()}), 500 