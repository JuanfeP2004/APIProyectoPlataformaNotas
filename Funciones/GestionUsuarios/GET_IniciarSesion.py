import os
import sys
import json
from datetime import datetime

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )


from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

GET_IniciarSesion = Blueprint('GET_IniciarSesion', __name__)

# Esta funcion recibe un GET con un form un JSON con los campos especificados:
# (email, contrasenia)
@GET_IniciarSesion.route('/IniciarSesion', methods=['GET'])
def AutenticarUsuario():
    try:

        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400    

        datos_json = json.loads(metadatos)

        email = datos_json['email']
        contrasenia = datos_json['contrasenia']

        coleccion_usr = mongo.db['Usuarios']

        autenticacion = [
            {"email": email},
            {"contrasenia": contrasenia}
        ]

        inicio_sesion = coleccion_usr.find_one({"$and": autenticacion})

        if not inicio_sesion:
            return jsonify({'error': 'El correo o la contraseña es incorrecto'}), 400


        documento = {
            "ultima_fecha_acceso": datetime.now(), 
        }

        resultado = mongo.db.Usuarios.update_one({"_id": inicio_sesion['_id']}, {"$set": documento})


        inicio_sesion['_id'] = str(inicio_sesion['_id'])
        inicio_sesion['universidad_id'] = str(inicio_sesion['universidad_id'])
        inicio_sesion['ultima_fecha_acceso'] = datetime.now()
        
        return jsonify(inicio_sesion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500