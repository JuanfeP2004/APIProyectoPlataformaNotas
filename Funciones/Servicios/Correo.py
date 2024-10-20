import os
from dotenv import load_dotenv

load_dotenv()

class Correo:
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')