from dotenv import load_dotenv
import jwt
import os
from bson.objectid import ObjectId


    
# Funcion para autenticar al usuario
def AutenticacionUsuario(request, roles):
    try:
        from app import mongo
        load_dotenv()

        request_token = request.headers.get('Authorization')

        if not request_token:
            return None

        # Decodificar el token
        token = str.split(request_token, ' ')[1]
        data = jwt.decode(token, os.getenv('LLAVE_AUTENTICACION'), algorithms=["HS256"])

        usuarios = mongo.db['Usuarios']
        id = ObjectId(data['user_id'])

        current_user = usuarios.find_one({'_id': id})

        if not current_user:
            return None
        
        if current_user['rol'] not in roles:
            return None
        
        return current_user

    except Exception:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    