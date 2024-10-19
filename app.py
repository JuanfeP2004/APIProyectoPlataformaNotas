# pip install azure-storage-blob
# pip install Flask-PyMongo
# pip install python-dotenv

# Correr: python -m flask run

from flask import Flask
from flask_pymongo import PyMongo 
from Funciones.Servicios.BaseDatos import Config

#from Funciones.Administracion.DEL_Comentario import DEL_Comentario
#from Funciones.Administracion.DEL_Documento import DEL_Documento
#from Funciones.Administracion.DEL_Usuario import DEL_Usuario

#from Funciones.Calificaciones.POST_AgregarCom import POST_AgregarCom

from Funciones.GestionDocumentos.POST_SubirDoc import POST_SubirDoc

from Funciones.GestionUsuarios.POST_CrearUsuario import POST_CrearUsuario
from Funciones.GestionUsuarios.PUT_EditarUsuario import PUT_EditarUsuario
from Funciones.GestionUsuarios.GET_IniciarSesion import GET_IniciarSesion


app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

#app.register_blueprint(DEL_Comentario)
#app.register_blueprint(DEL_Documento)
#app.register_blueprint(DEL_Usuario)

#app.register_blueprint(POST_AgregarCom)

app.register_blueprint(POST_SubirDoc)

app.register_blueprint(POST_CrearUsuario)
app.register_blueprint(PUT_EditarUsuario)
app.register_blueprint(GET_IniciarSesion)
