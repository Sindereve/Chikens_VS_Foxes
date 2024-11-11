import arcade

CELL_SIZE = 100

class Chicken(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y
        # position in grid
        self.grid_position = (x, y)
        # Selected chicken
        self.selected = False
    
    def move(self, new_x, new_y):
        self.center_x = new_x*CELL_SIZE+CELL_SIZE/2
        self.center_y = new_y*CELL_SIZE+CELL_SIZE/2
        self.grid_position = (new_x, new_y)

    def on_click(self):
        self.selected = not self.selected

class Fox(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y
        self.grid_position = (x, y)

    def move(self, new_x, new_y):
        self.center_x = new_x * CELL_SIZE + CELL_SIZE / 2
        self.center_y = new_y * CELL_SIZE + CELL_SIZE / 2
        self.grid_position = (new_y, new_x)

class Plant(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y
        self.grid_position = (x, y)
