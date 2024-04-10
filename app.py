from dotenv import load_dotenv
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routers import ClientRouter

import os, sys


class SocioClubApp:

    def __init__(self):
            self.app = FastAPI()
            self.setup_routes()
            self.setup_middleware()

    def setup_routes(self):
        self.app.include_router(ClientRouter.router)

    def setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )

    def run(self, host="localhost", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    my_app = SocioClubApp()
    host = input('Digite o host (Digite 1 para localhost): ')

    if host == '1':
        host = 'localhost'
    my_app.run(host=host)









