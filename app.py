from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routers import (
    ClientRouter,
    AuthRouter,
    ClubRouter,
    EventRouter,
    NewsRouter,
    ClubCategoryRouter,
    ProductRouter,
    PlanRouter,
    TicketRouter,
    StripeRouter,
)
import sys
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from services.ClientService import ClientService

full_path = os.path.abspath(os.path.join("./", '.env'))
path_env_file = full_path if os.path.isfile(full_path) else os.path.abspath(os.path.join(os.path.dirname(sys.executable), '.env'))

if load_dotenv(path_env_file):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
else:
    raise Exception('Não foi possível achar o arquivo .env: ' + path_env_file)

app = FastAPI()

app.include_router(ClientRouter.router)
app.include_router(AuthRouter.router)
app.include_router(ClubRouter.router)
app.include_router(NewsRouter.router)
app.include_router(ClubCategoryRouter.router)
app.include_router(ProductRouter.router)
app.include_router(PlanRouter.router)
app.include_router(EventRouter.router)
app.include_router(TicketRouter.router)
app.include_router(StripeRouter.router, prefix="/stripe", tags=["Stripe"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Middleware de autenticação JWT (mantido comentado como solicitado)
# @app.middleware('http')
# async def verify_token(request: Request, call_next):
#     if request.url.path == "/login" or request.url.path == "/register":
#             response = await call_next(request)
#             return response
#     try:
#             access_token = request.headers.get("Authorization")
#             if access_token is None:
#                 return JSONResponse(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     content={'error': 'Invalid token'}
#                 )
#             data = jwt.decode(access_token.split(' ')[1], SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={'error': 'Invalid token'}
#         )
#     client_on_db = ClientService.find_client_by_email(data['sub'])
#     if client_on_db is None:
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={'error': 'Invalid token'}
#         )
#     response = await call_next(request)
#     return response

def run(host="localhost", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    host = input('Digite o host (Digite 1 para localhost): ')
    if host == '1':
        host = 'localhost'
    run(host=host)
