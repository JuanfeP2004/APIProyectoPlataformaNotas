# pip install azure-storage-blob
# pip install Flask-PyMongo
# pip install python-dotenv
# pip install Flask-Mail
# pip install flask-bcrypt
# pip install PyJWT

# Correr: python -m flask run

from flask import Flask
from flask_pymongo import PyMongo 
from flask_mail import Mail
from Funciones.Servicios.BaseDatos import Config
from Funciones.Servicios.Correo import Correo
from flask_bcrypt import Bcrypt
from flask_cors import CORS


from Funciones.Administracion.DEL_BorrarCal import DEL_Comentario
from Funciones.Administracion.DEL_Documento import DEL_Documento
from Funciones.Administracion.DEL_BorrarUsuario import DEL_BorrarUsuario
from Funciones.Administracion.POST_AprobarDoc import POST_AprobarDoc
from Funciones.Administracion.GET_BuscarTodosDocs import GET_BuscarTodosDocs

from Funciones.Busqueda.GET_BuscarDocs import GET_BuscarDocs
from Funciones.Busqueda.POST_FiltrarDocs import GET_FiltrarDocs
from Funciones.Busqueda.POST_BuscarMisDocs import GET_BuscarMisDocs

from Funciones.Calificaciones.POST_AgregarCal import POST_AgregarCal
#from Funciones.Calificaciones.POST_DescargarDoc import POST_DescargarDoc
from Funciones.Calificaciones.POST_ReportarDoc import POST_ReportarDoc

from Funciones.GestionDocumentos.POST_SubirDoc import POST_SubirDoc
from Funciones.GestionDocumentos.PUT_EditarDoc import PUT_EditarDoc
from Funciones.GestionDocumentos.POST_ObtenerDoc import GET_ObtenerDoc

from Funciones.GestionUsuarios.POST_CrearUsuario import POST_CrearUsuario
from Funciones.GestionUsuarios.PUT_EditarUsuario import PUT_EditarUsuario
from Funciones.GestionUsuarios.POST_IniciarSesion import GET_IniciarSesion
from Funciones.GestionUsuarios.POST_RecuperarCon import GET_RecuperarCon


app = Flask(__name__)
app.config.from_object(Config)

CORS(app=app, resources={r"/*": {"origins":"*"}})

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = Correo.EMAIL
app.config['MAIL_PASSWORD'] = Correo.PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Correo.EMAIL

mongo = PyMongo(app)
mail = Mail(app)
bcrypt = Bcrypt(app)


app.register_blueprint(DEL_Comentario)
app.register_blueprint(DEL_Documento)
app.register_blueprint(DEL_BorrarUsuario)
app.register_blueprint(POST_AprobarDoc)
app.register_blueprint(GET_BuscarTodosDocs)

app.register_blueprint(GET_BuscarDocs)
app.register_blueprint(GET_FiltrarDocs)
app.register_blueprint(GET_BuscarMisDocs)

app.register_blueprint(POST_AgregarCal)
#app.register_blueprint(POST_DescargarDoc)
app.register_blueprint(POST_ReportarDoc)

app.register_blueprint(POST_SubirDoc)
app.register_blueprint(PUT_EditarDoc)
app.register_blueprint(GET_ObtenerDoc)

app.register_blueprint(POST_CrearUsuario)
app.register_blueprint(PUT_EditarUsuario)
app.register_blueprint(GET_IniciarSesion)
app.register_blueprint(GET_RecuperarCon)
