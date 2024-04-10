import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import sys

full_path = os.path.abspath(os.path.join("./",'.env'))
print(full_path)
path_env_file = full_path if os.path.isfile(full_path) else os.path.abspath(os.path.join(os.path.dirname(sys.executable), '.env'))

if load_dotenv(path_env_file):
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + path_env_file)

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        print("Conexão ao PostgreSQL bem-sucedida")
        return connection
    except (Exception, Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None
