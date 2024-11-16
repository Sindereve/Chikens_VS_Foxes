import arcade

from config import load_config
from gridObj import Chicken, Fox, Plant
import os

config = load_config()
# SCREEN
SCREEN_WIDTH = int(config["general"]["screen_width"])
SCREEN_HEIGHT =  int(config["general"]["screen_height"])

# Grid set
GRID_SIZE = int(config["grid"]["grid_size"])
CELL_SIZE = int(config["grid"]["cell_size"])

# edge
LEFT_EDGE_GRID = int(config["grid"]["left_edge"])
RIGHT_EDGE_GRID = GRID_SIZE * CELL_SIZE + LEFT_EDGE_GRID

# edge
DOWN__EDGE_GRID = int(config["grid"]["down_edge"])
UP_EDGE_GRID = GRID_SIZE * CELL_SIZE + DOWN__EDGE_GRID

class GameGrid:
    def __init__(self, grid_size=GRID_SIZE):
        
        
    def create_objects(self, game_grid):
        
    def draw(self):
        """Отрисовывает поле и все объекты"""
        

       