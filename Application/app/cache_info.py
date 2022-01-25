from math import floor
from typing import Any, List
from django.core.cache import cache
from app.models import Game, Tile
import numpy as np

_GAME = 'GAME'
_TILES = 'TILES'
_EMPTY = 'EMPTY'
_NEIGHBOURS = 'NEIGHBOURS'

def cache_game(game : Game):
    cache.set(_GAME, game)
    
def cache_tiles(array : list):
    cache.set(_TILES, array)

    # find current EMPTY
    empty_index = next((i for i, item in enumerate(array) if item.x == 0 and item.y == 0), ValueError)
    cache.set(_EMPTY, empty_index)
    print('INDEX', empty_index)
    cache_neighbours_from_empty(empty_index, array)

def get_cached_game() -> Game:
    return cache.get(_GAME)

def get_cached_tiles() -> list:
    return cache.get(_TILES)

def get_cached_empty() -> int:
    return cache.get(_EMPTY)

def get_cached_neighbours():
    return cache.get(_NEIGHBOURS)

def cache_neighbours_from_empty(empty_index : int, array : list):
    # find neighbours of current EMPTY
    current_neighbours = get_cached_neighbour_grid(3)[empty_index]
    cache.set(_NEIGHBOURS, current_neighbours)

def get_cached_neighbour_grid(n : int):
    key = 'n' + str(n)
    if cache.get(key) is None:
        all_neighbours = []
        grid_items = []
        for i in range(n * n):
            grid_items.append(GridItems(i, n))

        for i in grid_items:
            neighbours = []
            # add in same column
            for j in get_neighbours_part(n, i.y):
                neighbours.append(i.x + j * n)
            # add on same row
            for j in get_neighbours_part(n, i.x):
                neighbours.append(j + i.y * n)
            all_neighbours.append(neighbours)
        
        cache.set(key, all_neighbours)
    return cache.get(key)

def get_neighbours_part(n : int, current_part : int) -> List:
    neighbours = []
    if current_part == 0:
        neighbours.append(current_part + 1)
    elif current_part == n - 1:
        neighbours.append(current_part - 1)
    else:
        neighbours.append(current_part + 1)
        neighbours.append(current_part - 1)
    return neighbours
    
def clear_cache():
    pass
    # cache.delete(_GAME)
    # cache.delete(_TILES)
    # cache.delete(_EMPTY)
    # cache.delete(_NEIGHBOURS)

class GridItems:
    def __init__(self, i : int, n : int):
        self.x = i % n
        self.y = floor(i / n)
