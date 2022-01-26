from io import BytesIO
from linecache import cache
from math import floor
from PIL import Image
from django.core.files import File
from app.models import Game, PlayImage, Tile
import random
from app.cache_info import cache_game, cache_tiles, get_cached_empty, get_cached_neighbours, get_cached_tiles
from app.common import GameInfo, get_game_info, swap_tiles

def slice_image(
    play_image: PlayImage
):
    n = play_image.level
    img = Image.open(play_image.image)
    image_to_use = img
    w, h = img.size

    # crashes if > 300px
    
    if w > 300 or h > 300:
        ratio = 1
        if w > h:
            ratio = 300 / w
        else:
            ratio = 300 / h
        w = floor(w * ratio)
        h = floor(h * ratio)
        
        size = (w, h)
        image_to_use.thumbnail(size)

    default_array = []
    
    tile_width = int(floor(w / n))
    tile_height = int(floor(h / n))
    x_index = y_index = 0
    for x in range(0, w, tile_width):
        y_index = 0
        for y in range(0, h, tile_height):
            image_to_use = img
            is_blank = False
            size = (tile_width, tile_height)
            if x == 0 and y == 0:
                is_blank = True
                blank = PlayImage.objects.get(title = 'BLANK')
                image_to_use = Image.open(blank.image)

            box = (x, y,
                x + tile_width if x + tile_width < w else w - 1,
                y + tile_height if y + tile_height < h else h - 1)
            img_piece = image_to_use.crop(box)

            thumb_io = BytesIO() # create a BytesIO object

            img_piece.save(thumb_io, 'JPEG', quality = 85)
            tile = Tile.objects.create(x=x_index, y= y_index
                                    , parent=play_image
                                    , image = File(thumb_io, name=f'{play_image.id}_{x_index}_{y_index}')
                                    , is_blank = is_blank)
            default_array.append(tile)
            y_index += 1
        x_index += 1 
    return default_array

def start_game(request, play_image) -> GameInfo:
    n = play_image.level

    # GET  array of tiles
    tiles = list(Tile.objects.filter(parent = play_image))
    default_array = []
    if len(tiles) > 0:
        default_array = tiles
    else:
        default_array = slice_image(play_image)

    game = Game.objects.create(user = request.user, play_image = play_image)

    cache_game(game)
    cache_tiles(default_array)
    tiles = get_cached_tiles()
    previous = get_cached_empty()
    for c in list(range(0, n * n)):
        empty = get_cached_empty()
        neighbours = get_cached_neighbours()

        # Making sure we don't keep swapping the same items
        i = random.randrange(0, len(neighbours))
        i_index = neighbours[i]
        if i_index == previous:
            if i + 1 >= len(neighbours):
                i = 0
            else:
                i += 1
        previous = empty
        tiles = swap_tiles(tiles, empty, neighbours[i])

    cached_tiles = get_cached_tiles()
    return get_game_info(game, cached_tiles)


