from app.cache_info import cache_tiles, clear_cache, get_cached_empty, get_cached_game, get_cached_neighbours, get_cached_tiles
from app.models import Tile, Game
from app.common import GameInfo, get_game_info, swap_tiles

def validate(game_id : int):
    game = get_cached_game()
    tiles = get_cached_tiles()
    for index, t in enumerate(tiles):
        if validate_tile(index, t, game.play_image.level) == False:
            return False

    #clear cache if valid
    clear_cache()
    return True

def validate_tile(index : int, tile : Tile, n : int):
    return True if tile.x * n + tile.y == index else False

def do_one_move(tile_id : int) -> GameInfo:
    game = get_cached_game()
    tiles = get_cached_tiles()
    empty = get_cached_empty()
    neighbours = get_cached_neighbours()

    clicked = -1
    print("tile id ", tile_id)
    print("tile", neighbours)
    for index, t in enumerate(tiles):
        print(t.id)
        if t.id == tile_id:
            clicked = index
            break
 
    print("clicked ", clicked)
    if clicked in neighbours:
        tiles = swap_tiles(tiles, empty, clicked)
    return get_game_info(game, tiles)
