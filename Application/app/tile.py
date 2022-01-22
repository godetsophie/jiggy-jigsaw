from PIL import Image


class Tile():
    image : Image = None
    x = y = 0
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    