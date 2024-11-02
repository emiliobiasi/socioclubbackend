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
    PlanRouter,
    TicketRouter,
)
import sys
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from services.ClientService import ClientService
from src.modules.images.external.datasource.image_datasource import ImageDatasource
from src.modules.images.external.repositories.image_repository import ImageRepository

from src.modules.products.routers import product_router as ProductRouter
from src.modules.images.external.routers.image_router import ImageRouter
from src.modules.stripe.routers import StripeRouter
import os

full_path = os.path.abspath(os.path.join("./", ".env"))
path_env_file = (
    full_path
    if os.path.isfile(full_path)
    else os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".env"))
)

if load_dotenv(path_env_file):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_KEY_PATH')

else:
    raise Exception("Não foi possível achar o arquivo .env: " + path_env_file)

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

# TODO - Estudar injeção de dependencias
app.include_router(
    ImageRouter(
        repo=ImageRepository(
            datasource=ImageDatasource(
                bucket_name=BUCKET_NAME,
            ),
        )
    ).router
)

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port="8000",
    )
