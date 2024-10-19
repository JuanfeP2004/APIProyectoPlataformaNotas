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

from Funciones.Calificaciones.POST_AgregarCal import POST_AgregarCal
from Funciones.Calificaciones.POST_DescargarDoc import POST_DescargarDoc
from Funciones.Calificaciones.POST_ReportarDoc import POST_ReportarDoc

from Funciones.GestionDocumentos.POST_SubirDoc import POST_SubirDoc
from Funciones.GestionDocumentos.PUT_EditarDoc import PUT_EditarDoc
from Funciones.GestionDocumentos.GET_ObtenerDoc import GET_ObtenerDoc

from Funciones.GestionUsuarios.POST_CrearUsuario import POST_CrearUsuario
from Funciones.GestionUsuarios.PUT_EditarUsuario import PUT_EditarUsuario
from Funciones.GestionUsuarios.GET_IniciarSesion import GET_IniciarSesion


app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

#app.register_blueprint(DEL_Comentario)
#app.register_blueprint(DEL_Documento)
#app.register_blueprint(DEL_Usuario)

app.register_blueprint(POST_AgregarCal)
app.register_blueprint(POST_DescargarDoc)
app.register_blueprint(POST_ReportarDoc)

app.register_blueprint(POST_SubirDoc)
app.register_blueprint(PUT_EditarDoc)
app.register_blueprint(GET_ObtenerDoc)

app.register_blueprint(POST_CrearUsuario)
app.register_blueprint(PUT_EditarUsuario)
app.register_blueprint(GET_IniciarSesion)
