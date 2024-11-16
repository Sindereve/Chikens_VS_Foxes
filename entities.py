import arcade

# size one cell
CELL_SIZE = 100


class Object_Cell(arcade.Sprite):
    def __init__(self, x, y, texture_path):
        super().__init__(texture_path)
        self.center_x = x
        self.center_y = y

        # position in grid
        self.grid_position = (int(x // CELL_SIZE), int(y // CELL_SIZE)) 

        # size for drow
        scale_x = CELL_SIZE / self.width
        scale_y = CELL_SIZE / self.height
        self.scale = min(scale_x, scale_y)

        

class Chicken(Object_Cell):
    def __init__(self, x, y, texture_path):
        super().__init__(x, y, texture_path)
        # Selected chicken
        self.selected = False
        
    
    def move(self, new_x, new_y):
        print('\n-----------Job move func-----------')
        self.center_x = new_x*CELL_SIZE+CELL_SIZE/2
        self.center_y = new_y*CELL_SIZE+CELL_SIZE/2
        print('Centet x/y', self.center_x, self.center_y)
        self.grid_position = (new_x, new_y)
        print('New x/y', new_x, new_y)
        print('\n-----------Job move func-----------')

    def on_click(self):
        self.selected = not self.selected

    def draw(self):
        super().draw()

        # Draw a border around the chicken if it's selected
        if self.selected:
            arcade.draw_rectangle_outline(self.center_x, self.center_y, CELL_SIZE, CELL_SIZE, arcade.color.RED, 5)

    

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
