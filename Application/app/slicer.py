from io import BytesIO
import os
from math import floor
from telnetlib import GA
from xmlrpc.client import boolean
from PIL import Image
from django.core.files import File
from app.models import Game, GameTile, PlayImage, Tile
from python_webapp_django.settings import MEDIA_ROOT, MEDIA_URL
import random

class GameInfo:
    def __init__(self, game : Game, game_tiles : list):
        self.game = game
        self.game_tiles = game_tiles 

n = 3
def slice_image(
    play_image: PlayImage
):
    img = Image.open(play_image.image)
    image_to_use = img
    w, h = img.size

    default_array = []
    
    tile_width = int(floor(w / n))
    tile_height = int(floor(h / n))
    x_index = y_index = 0
    for x in range(0, w, tile_width):
        y_index = 0
        for y in range(0, h, tile_height):
            image_to_use = img
            is_blank = False
            if x == 0 and y == 0:
                is_blank = True
                blank = PlayImage.objects.get(title = 'BLANK')
                image_to_use = Image.open(blank.image)

            box = (x, y,
                x + tile_width if x + tile_width < w else w - 1,
                y + tile_height if y + tile_height < h else h - 1)
            img_piece = image_to_use.crop(box)

            thumb_io = BytesIO() # create a BytesIO object

            img_piece.save(thumb_io, 'JPEG')
            tile = Tile.objects.create(x=x_index, y= y_index
                                    , parent=play_image
                                    , image = File(thumb_io, name=f'{play_image.id}_{x_index}_{y_index}')
                                    , is_blank = is_blank)
            default_array.append(tile)
            y_index += 1
        x_index += 1 

    return default_array

def mix_array(request, play_image) -> GameInfo:
    print('in mix_array')
    tiles = Tile.objects.filter(parent = play_image)
    default_array = []
    if len(tiles) > 0:
        default_array = tiles
    else:
        default_array = slice_image(play_image)

    game = Game.objects.create(user = request.user, play_image = play_image)

    game_tiles = []
    for tile in default_array:
        game_tile = GameTile.objects.create(game = game, tile = tile, current_x = tile.x, current_y = tile.y)
        game_tiles.append(game_tile)

    empty = get_empty(game_tiles)
    previous = empty
    for c in list(range(0, 2)):
        empty = get_empty(game_tiles)
        print(empty.tile.image)
        neighbours = get_neighbours(game_tiles, empty, previous)
        print(neighbours)
        i = random.randrange(0, len(neighbours))
        previous = neighbours[i]
        swap(empty, previous)

    return GameInfo(game, get_2d_array(game_tiles, n))

def check_swap(game_tile : GameTile):
    game_tiles = GameTile.objects.filter(game = game_tile.game)
    m = game_tile.game.play_image.level
    empty = get_empty(game_tiles)
    if are_neighbours(game_tile, empty):
        swap(game_tile, empty)
        game_tiles = GameTile.objects.filter(game = game_tile.game)
        empty = get_empty(game_tiles)
    
    return GameInfo(game_tile.game, get_2d_array(game_tiles, m))

def get_2d_array(game_tiles, m:int):
    output_array = []
    for i in range(0, m):
        d1 = []
        for j in range(0, m):
            d1.append(game_tiles[0])
        output_array.append(d1)
    
    for t in game_tiles:
        output_array[t.current_y][t.current_x] = t
    return output_array

def get_empty(array: list) -> GameTile:
    empty = None
    for a in array:
        if a.tile.is_blank == True:
            empty = a
            break
    return empty

def get_neighbours(array: list, empty: GameTile, previous: GameTile):
    neighbours = []
    for a in array:
        if a.id != previous.id and are_neighbours(a, empty):
            print(a.current_x, a.current_y)
            neighbours.append(a)
    return neighbours

def are_neighbours(a: GameTile, b: GameTile) -> boolean:
    if (a.current_x == b.current_x and (a.current_y == b.current_y-1 or a.current_y == b.current_y+1)) or (a.current_y == b.current_y and (a.current_x == b.current_x-1 or a.current_x == b.current_x+1)):
        return True
    return False
            
def swap(a: GameTile, b : GameTile):
    a.current_x, b.current_x = b.current_x, a.current_x
    a.current_y, b.current_y = b.current_y, a.current_y
    a.save()
    b.save()

def validate_game(game : Game):
    game_tiles = GameTile.objects.filter(game = game)
    for t in game_tiles:
        if t.current_x != t.tile.x or t.current_y != t.tile.y:
            return False
    return True
