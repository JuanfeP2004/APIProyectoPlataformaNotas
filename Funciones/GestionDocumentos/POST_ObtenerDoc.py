import os
import sys
import io
import json
from bson.objectid import ObjectId
from flask_cors import cross_origin

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor
from Servicios.Autenticacion import AutenticacionUsuario

from flask import Blueprint, request, jsonify, send_file

GET_ObtenerDoc = Blueprint('GET_ObtenerDoc', __name__)

@GET_ObtenerDoc.route('/ObtenerDocumento', methods=['POST'])
@cross_origin()
def ObtenerDocumento():
    try:

        from app import mongo

        usuario = AutenticacionUsuario(request=request, roles=['usuario','admin'])

        if usuario is None:
            return jsonify({'error': 'Credenciales invalidas'}), 401

        if "json" not in request.form:
            return jsonify({'error': 'No se proporcionó un json'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400    

        datos_json = json.loads(metadatos)    

        id = ObjectId(datos_json['id'])

        coleccion_doc = mongo.db['documentos']

        existe_doc = coleccion_doc.find_one({'_id': id})

        if not existe_doc:
            return jsonify({'error': 'No existe ese documento'}), 400

        cliente = storage.get_blob_client(container=contenedor, blob=existe_doc['archivo'])
        archivo = cliente.download_blob().readall()

        documento = {
            "numero_descargas": existe_doc['numero_descargas'] + 1, 
        }

        resultado = coleccion_doc.update_one({"_id": id}, {"$set": documento})

        return send_file(io.BytesIO(archivo), download_name=existe_doc['archivo'], as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500