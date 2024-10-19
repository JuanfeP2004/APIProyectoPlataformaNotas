import os
import sys
import uuid
import json

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )
from Servicios.Storage import storage, contenedor
from app import mongo

from flask import Blueprint, request, jsonify
# Falta importar la funcion de base de datos

DEL_Usuario = Blueprint('DEL_Usuario', __name__)

# Esta funcion recibe un POST con un form que tiene un archivo y un JSON con los campos especificados:
# (nombre, tipo, materia, universidad)
@DEL_Usuario.route('/BorrarUsuario', methods=['DELETE'])
def BorrarUsuario():
    try:
        return 'Hola'
    except Exception as e:
        return jsonify({"error": str(e)}), 500 