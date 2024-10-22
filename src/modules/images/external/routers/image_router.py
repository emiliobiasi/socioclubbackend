from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from src.modules.images.external.repositories.image_repository import ImageRepository

class ImageRouter():

    def __init__(self, repo: ImageRepository):

        self.router = APIRouter()
        self.image_repo = repo

        self.set_routes()


    def set_routes(self):

        @self.router.post('/generate-img-url')
        async def generate_img_url(request: Request):   

            try:
                body = await request.json()

                filename = body['filename']

                url = self.image_repo.save_image(filename=filename)
                return JSONResponse(content={'url': url}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"message": f"Erro ao gerar url: {str(e)}"}, status_code=500)