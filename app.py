from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routers import ClientRouter

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

app.include_router(ClientRouter.router)
