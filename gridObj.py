import arcade
from tools import load_config

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


class Object_Cell(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y

        # position in grid
        self._grid_position = (int(x // CELL_SIZE - (LEFT_EDGE_GRID // CELL_SIZE)), int(y // CELL_SIZE)) 

        # size for drow
        scale_x = CELL_SIZE / self.width
        scale_y = CELL_SIZE / self.height
        self.scale = min(scale_x, scale_y)

    def move(self, new_x, new_y):
        self.center_x = new_x*CELL_SIZE+CELL_SIZE/2 + LEFT_EDGE_GRID
        self.center_y = new_y*CELL_SIZE+CELL_SIZE/2
        self._grid_position = (new_x, new_y)

    @property
    def typeOb(self):
        pass

    @property
    def grid_position(self):
        x, y = self._grid_position
        x =  x + LEFT_EDGE_GRID//CELL_SIZE - LEFT_EDGE_GRID//CELL_SIZE
        return x, y


        

class Chicken(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
        # Selected chicken
        self.selected = False
        self._name_class = 'Chicken'
        
    def on_click(self):
        self.selected = not self.selected
    
    @property
    def typeOb(self):
        return self._name_class

    def draw(self):
        super().draw()

        # Draw a border around the chicken if it's selected
        if self.selected:
            arcade.draw_rectangle_outline(self.center_x, self.center_y, CELL_SIZE, CELL_SIZE, arcade.color.RED, 5)

    

class Fox(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
        self._name_class = 'Fox'

    @property
    def typeOb(self):
        return self._name_class



class Plant(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
        self._name_class = 'Plant'

    @property
    def typeOb(self):
        return self._name_class

    
