import bcrypt
import psycopg2
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from database.connection.Connection import connect_to_db
from models.Clients import Clients

app = FastAPI()

origins = [
    "http://localhost/",
    "http://localhost:8080/",
    # Adicione aqui os domínios permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

EMPTY_STRING = "";

from fastapi.responses import JSONResponse


@app.get("/clients")
async def get_clients():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        clients_list = []
        for client in data:
            client_dict = {
                "id": client[0],
                "cpf": client[1],
                "name": client[2],
                "email": client[3],
                "password": client[4]
            }
            clients_list.append(client_dict)
        return JSONResponse(content={'clients': clients_list}, status_code=200)
    else:
        return JSONResponse(content={"message": "Falha na conexão ao PostgreSQL"}, status_code=500)


@app.post("/register", response_model=None)
async def insert_clients(client: Clients):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO clients (name, email, password) VALUES (%s, %s, %s);",
                           (client.name, client.email, create_hash_password(client.password)))
            connection.commit()
            cursor.close()
            connection.close()
            return JSONResponse(content={'data': 'Cliente inserido'}, status_code=201)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inserir cliente: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão ao PostgreSQL")


@app.delete("/delete/{cpf}")
async def delete_clients(cpf: str):
    connection = connect_to_db()
    print(cpf)
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM CLIENTS WHERE cpf = '{cpf}';")
            connection.commit()
            cursor.close()
            connection.close()
            return JSONResponse(content={'data': 'Cliente deletado'}, status_code=204)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão ao PostgreSQL")


@app.put("/update/{cpf}", response_model=Clients)
async def update_clients(cpf: str, client: Clients):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE CLIENTS SET NAME = '{client.name}', EMAIL = '{client.email}', PASSWORD = '{client.password}' WHERE CPF = '{cpf}';")
            connection.commit()
            cursor.close()
            connection.close()
            return JSONResponse(content={'data': 'Cliente atualizado com sucesso'}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail="Falha na conexão ao PostgreSQL")


@app.get("/findByCpf/{cpf}")
async def find_by_cpf(cpf: str):
    connection = connect_to_db()
    if cpfExists(cpf):
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM CLIENTS WHERE CPF = '{cpf}';")
                connection.commit()
                data = cursor.fetchall()
                cursor.close()
                connection.close()
                return JSONResponse(content={'data': data}, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao achar cliente: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail="Falha na conexão ao PostgreSQL")
    else:
        return JSONResponse(content={'data': 'Esse cliente nao existe na base de dados'}, status_code=404)


@app.get("/findById/{id}")
async def find_by_id(id: int):
    connection = connect_to_db()
    if idExists(id):
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM CLIENTS WHERE ID = {id};")
                connection.commit()
                data = cursor.fetchall()
                cursor.close()
                connection.close()
                return JSONResponse(content={'data': data}, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro ao achar cliente por id: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail="Falha na conexão ao PostgreSQL")
    else:
        return JSONResponse(content={'data': 'Esse cliente nao existe na base de dados'}, status_code=404)


def idExists(id_to_find: int) -> bool:
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS;")
        data = cursor.fetchall()
        for client in data:
            if id_to_find == client[0]:
                return True
        return False
    connection.close()


def cpfExists(cpf: str) -> bool:
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS;")
        data = cursor.fetchall()
        for client in data:
            if cpf == client[1]:
                return True
        return False
    connection.close()


def create_hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def teste() -> list:
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS;")
        data = cursor.fetchall()
        return data
    connection.close()
if __name__ == "__main__":
    for c in range(len(teste())):
        print(c)
        dicionario = {
            "id": c
        }
    print(dicionario)

