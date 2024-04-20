from fastapi import HTTPException, status
from services.ClientService import ClientService
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
from dotenv import dotenv_values

projeto_raiz = os.getcwd()
caminho_env = os.path.join(projeto_raiz, '.env')
env_vars = dotenv_values(caminho_env)

if load_dotenv(caminho_env):
    SECRET_KEY = env_vars.get("SECRET_KEY")
    ALGORITHM = env_vars.get("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + caminho_env)

class AuthService:

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