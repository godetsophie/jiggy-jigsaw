from typing import Any
from app.models import Game, Tile
import numpy as np

from app.cache_info import cache_tiles

class GameInfo:
    def __init__(self, game : Game, tiles : list):
        self.game = game
        self.tiles = tiles 

def get_game_info(game : Game, tiles : list) -> GameInfo:
    return GameInfo(game, get_2d_array(tiles, game.play_image.level))

def get_2d_array(game_tiles, m:int):
    arr = np.array(game_tiles)
    return np.transpose(arr.reshape(m, m))

def get_1d_array(game_tiles, m:int):
    return np.array.flatten(game_tiles) 

def swap_tiles(tiles : list, empty_index : int, previous_index : int) -> list:
    # swap features between empty and random: index
    empty = tiles[empty_index]
    previous = tiles[previous_index]
    tiles[previous_index] = empty
    tiles[empty_index] = previous
    cache_tiles(tiles)
    return tiles