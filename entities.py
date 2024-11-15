import arcade

# size one cell
CELL_SIZE = 100


class Object_Cell(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y

        # position in grid
        self.grid_position = (x, y)

        # size for drow
        target_width = CELL_SIZE
        target_height = CELL_SIZE
        scale_x = target_width / self.width
        scale_y = target_height / self.height
        self.scale = min(scale_x, scale_y)
        

class Chicken(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
        # Selected chicken
        self.selected = False
        
    
    def move(self, new_x, new_y):
        self.center_x = new_x*CELL_SIZE+CELL_SIZE/2
        self.center_y = new_y*CELL_SIZE+CELL_SIZE/2

        self.grid_position = (new_x, new_y)

    def on_click(self):
        self.selected = not self.selected

class Fox(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)

    def move(self, new_x, new_y):
        self.center_x = new_x * CELL_SIZE + CELL_SIZE / 2
        self.center_y = new_y * CELL_SIZE + CELL_SIZE / 2
        self.grid_position = (new_x, new_y)

class Plant(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
