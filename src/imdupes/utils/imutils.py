import PIL.Image


class ImageFileWrapper:
    def __init__(self, image: PIL.Image, path: str):
        self.image = image
        self.path = path
