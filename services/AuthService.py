from fastapi import HTTPException, Request, status
from services.ClientService import ClientService
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os, sys
from dotenv import load_dotenv

full_path = os.path.abspath(os.path.join("./",'.env'))
path_env_file = full_path if os.path.isfile(full_path) else os.path.abspath(os.path.join(os.path.dirname(sys.executable), '.env'))

if load_dotenv(path_env_file):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + path_env_file)

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
    
    @staticmethod
    async def verify_token(request: Request, call_next):

        if request.url.path == "/login":
        # Se for a rota de login, não faz a verificação do token e continua para o próximo middleware
            response = await call_next(request)
            return response
        
        try:
            access_token = request.headers.get("Authorization")

            if access_token is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token inválido'
                )

            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido'
            )
        
        client_on_db = ClientService.find_client_by_email(data['sub'])

        if client_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido'
            )
        
        response = await call_next(request)
        return response