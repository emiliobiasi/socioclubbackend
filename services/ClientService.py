from typing import List, Optional

from models.Clients import Clients
from database.connection.Connection import connect_to_db
import bcrypt


class ClientService:
    @staticmethod
    def get_clients() -> List[Clients]:
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
                    Clients(id=client[0], cpf=client[1], name=client[2], email=client[3], password=client[4]))
            return clients_list
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def find_by_id(client_id: int) -> Optional[Clients]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM CLIENTS WHERE id={client_id};")
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Clients(id=data[0], cpf=data[1], name=data[2], email=data[3], password=data[4])
            else:
                return None
        else:
            raise Exception("Falha na conexão ao PostgreSQL")

    @staticmethod
    def insert_client(client: Clients) -> None:
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
    def update_client_by_cpf(cpf: str, client: Clients) -> None:
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
    def find_client_by_cpf(cpf: str) -> Optional[Clients]:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM CLIENTS WHERE cpf = %s;", (cpf,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return Clients(id=data[0], cpf=data[1], name=data[2], email=data[3], password=data[4])
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
