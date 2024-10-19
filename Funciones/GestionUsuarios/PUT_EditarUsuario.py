import os
import sys
import json
from bson.objectid import ObjectId

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )


from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

PUT_EditarUsuario = Blueprint('PUT_EditarUsuario', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (id, nombre, email, contrasenia, universidad)
@PUT_EditarUsuario.route('/EditarUsuario', methods=['PUT'])
def EditarUsuario():
    try:
        from app import mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400    

        datos_json = json.loads(metadatos)

        id = ObjectId(datos_json['id'])
        nombre = str.upper(datos_json['nombre'])
        email = datos_json['email']
        contrasenia = datos_json['contrasenia']
        universidad = datos_json['universidad']

        # Validaciones

        if nombre in (None, ''):
            return jsonify({'error': 'El nombre no puede estar en blanco o vacio'}), 400
        if email in (None, ''):
            return jsonify({'error': 'El email no puede estar en blanco o vacio'}), 400
        if contrasenia in (None, ''):
            return jsonify({'error': 'La contraseña no puede estar en blanco o vacia'}), 400

        coleccion = mongo.db['Usuarios']
        universidades = mongo.db['universidades']

        existe_usuario = coleccion.find_one({"_id": id})

        if not existe_usuario:
            return jsonify({'error': 'No existe ese usuario'}), 400

        condiciones = [
            {"nombre": nombre},
            {"email": email}
        ]

        val_usuario = coleccion.find_one({"$or": condiciones})

        if val_usuario and val_usuario['_id'] != id:
            return jsonify({'error': 'Ya existe otro usuario con ese nombre o correo'}), 400

        val_uni = universidades.find_one({"nombre": universidad})

        if not val_uni:
            return jsonify({'error': 'No existe esa universidad'}), 400


        documento = {
            "nombre_completo": nombre, 
            "email": email,
            "contrasenia": contrasenia,
            "universidad_id": val_uni['_id'],
        }

        resultado = mongo.db.Usuarios.update_one({"_id": id}, {"$set": documento})

        return jsonify({"ok": "se actualizo el usuario correctamente"}), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500