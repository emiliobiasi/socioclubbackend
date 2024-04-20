from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import JWTError
from routers import ClientRouter, AuthRouter
from fastapi import Request
from services.ClientService import ClientService
import sys, os
from dotenv import load_dotenv
from jose import jwt

full_path = os.path.abspath(os.path.join("./",'.env'))
path_env_file = full_path if os.path.isfile(full_path) else os.path.abspath(os.path.join(os.path.dirname(sys.executable), '.env'))

if load_dotenv(path_env_file):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
else:
   raise Exception('Não foi possível achar o arquivo .env: ' + path_env_file)

app = FastAPI()

app.include_router(ClientRouter.router)
app.include_router(AuthRouter.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware('http')
async def verify_token(request: Request, call_next):
    
    if request.url.path == "/login" or request.url.path == "/register":
            response = await call_next(request)
            return response
    try:
            access_token = request.headers.get("Authorization")

            print(access_token)

            if access_token is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={'error': 'Invalid token'}
                )

            data = jwt.decode(access_token.split(' ')[1], SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'error': 'Invalid token'}
        )
        
    client_on_db = ClientService.find_client_by_email(data['sub'])

    if client_on_db is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'error': 'Invalid token'}
        )
    
    response = await call_next(request)
    return response


def run(host="localhost", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    host = input('Digite o host (Digite 1 para localhost): ')

    if host == '1':
        host = 'localhost'
    run(host=host)









