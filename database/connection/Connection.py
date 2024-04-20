import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

projeto_raiz = os.getcwd()

caminho_env = os.path.join(projeto_raiz, '.env')

if load_dotenv(caminho_env):
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

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
