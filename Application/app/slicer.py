import os
from math import sqrt, ceil, floor
from PIL import Image
from app.tile import Tile
  
def slice_image(
    im: Image,
    rows=3,
    columns=3,
):

    im_w, im_h = im.size

    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h):  # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w):  # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1, int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, pos_x, pos_y)
            tiles.append(tile)
            number += 1
    return tuple(tiles)
