from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import status, HTTPException
from models.Client import Client
from database.connection.Connection import connect_to_db
import bcrypt
import os
from dotenv import load_dotenv
from jose import jwt, JWTError

#Fazer tratamento de erro nos services usando HTTPException
#Ver Exceptions que podem ser lançadas pelo postgres
#Seguir o vídeo https://www.youtube.com/watch?v=c1vTa6WIMTg
#Ver uma forma de juntar os find em um só método
#Ver outra forma de importar variáveis de ambiente

full_path = os.path.abspath(os.path.join("./",'.env'))
path_env_file = full_path if os.path.isfile(full_path) else os.path.abspath(os.path.join(os.path.dirname(sys.executable), '.env'))

if load_dotenv(path_env_file):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + path_env_file)

class ClientService:

    @staticmethod
    def login(email:str, password:str , expires_at=30):
        
        client_on_db = ClientService.find_client_by_email(email)

        if client_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Email ou senha incorretos',
            )
        
        if not ClientService.verify_password(password, client_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Email ou senha incorretos',
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_at)

        payload = {
            'sub': email,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'expires_at': exp.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @staticmethod
    def get_clients() -> List[Client]:

        connection = connect_to_db()
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLIENTS;")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            clients_list = []
            for client in data:
                clients_list.append(
                    Client(id=client[0], cpf=client[1], name=client[2], email=client[3], password=client[4]))
            return clients_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def find_by_id(client_id: int) -> Optional[Client]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM CLIENTS WHERE id={client_id};")
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Client(id=data[0], cpf=data[1], name=data[2], email=data[3], password=data[4])
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def insert_client(client: Client) -> None:
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO clients (name, email, password) VALUES (%s, %s, %s);",
                               (client.name, client.email, ClientService.create_hash_password(client.password)))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                raise Exception(f"Erro ao inserir cliente: {str(e)}")
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def delete_client_by_cpf(cpf: str) -> None:
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM CLIENTS WHERE cpf = %s;", (cpf,))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                raise Exception(f"Erro ao deletar cliente: {str(e)}")
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def update_client_by_cpf(cpf: str, client: Client) -> None:
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE CLIENTS SET NAME = %s, EMAIL = %s, PASSWORD = %s WHERE CPF = %s;",
                               (client.name, client.email, client.password, cpf))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                raise Exception(f"Erro ao atualizar cliente: {str(e)}")
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def find_client_by_cpf(cpf: str) -> Optional[Client]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLIENTS WHERE cpf = %s;", (cpf,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Client(id=data[0], cpf=data[1], name=data[2], email=data[3], password=data[4])
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")
        
    @staticmethod
    def find_client_by_email(email: str) -> Optional[Client]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLIENTS WHERE email = %s;", (email,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Client(id=data[0], cpf=data[1], name=data[2], email=data[3], password=data[4])
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    def create_hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password.decode('utf-8')

    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
