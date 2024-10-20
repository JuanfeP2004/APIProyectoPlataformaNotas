import os
import sys
import json
import uuid
from flask_mail import Message

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )


from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

GET_RecuperarCon = Blueprint('GET_RecuperarCon', __name__)

# Esta funcion recibe un GET con un form un JSON con los campos especificados:
# (email, contrasenia)
@GET_RecuperarCon.route('/RecuperarContrasenia', methods=['GET'])
def AutenticarUsuario():
    try:

        from app import mail, mongo

        if 'json' not in request.form:
            return jsonify({'error': 'No se proporcionó un JSON'}), 400

        metadatos = request.form['json']

        if not metadatos:
            return jsonify({'error': 'El JSON esta mal'}), 400    

        datos_json = json.loads(metadatos)

        email = datos_json['email']

        usuarios = mongo.db['Usuarios']

        existe = usuarios.find_one({'email': email})
        if not existe:
            return jsonify({'error': 'No existe un usuario con ese correo'})

        codigo = str(uuid.uuid4())

        correo = Message(
            "Recuperar Contraseña",
            recipients=[email]
        )

        correo.body = f"Para recuperar su cuenta acabamos de actualizar su contraseña, la cual es: {codigo}"
    
        mail.send(correo)

        nueva_contrasenia = {
            "contrasenia": codigo
        }

        usuarios.update_one({'email': email}, {"$set": nueva_contrasenia})

        return jsonify({'ok': f'Se acaba de enviar un correo de recuperacion a {email}'})

    except Exception as e:
        return jsonify({"error": str(e)}), 500