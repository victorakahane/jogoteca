from dotenv import load_dotenv
from os import getenv
import os

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = getenv('SGBD'),
        usuario = getenv('USER'),
        senha = getenv('PASSWORD'),
        servidor = getenv('HOST'),
        database = getenv('DATABASE')
    )

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\uploads'
