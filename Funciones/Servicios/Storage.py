import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()
cadena_conexion = os.getenv('STORAGE')
storage = BlobServiceClient.from_connection_string(cadena_conexion)
contenedor = os.getenv('CONTAINER')