import arcade
from config import load_config
from gridObj import Chicken, Fox, Plant
from gameGrid import GameGrid
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


ASSETS_PATH = os.path.join(os.path.dirname(__file__), str(config["assets"]["assets_path"]))

class Game(arcade.Window):
    """
        Main app class
    """    

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chickens VS Fox")
        arcade.set_background_color(arcade.csscolor.WHITE)
        # Create Grid
        self._gameGrid = GameGrid()

        
    def setup(self):
        """Set up the game."""
        pass

    def on_draw(self):
        """Render the screen"""
        # Clear screen
        arcade.start_render()
        self._gameGrid.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Click mouse"""
        self._gameGrid.on_mouse_press(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        """Handle key presses for moving the selected chicken"""
        self._gameGrid.on_key_press(symbol, modifiers)
        self.on_draw()

    # self.on_draw()
    def update(self, delta_time):
        """ Update sprite """
        pass

def main():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    main()