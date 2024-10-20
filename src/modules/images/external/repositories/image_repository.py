from src.modules.images.external.datasource.image_datasource import ImageDatasource

class ImageRepository():

    def __init__(self, datasource: ImageDatasource):
        self.datasource = datasource

    def save_image(self, filename):
        return self.datasource.generate_signed_url(
            file_name=filename
        )
