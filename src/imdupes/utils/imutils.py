import PIL.Image


class ImageFileWrapper:
    def __init__(self, image: PIL.Image = None, path: str = None):
        self.image = image
        self.path = path
