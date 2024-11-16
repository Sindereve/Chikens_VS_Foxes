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


ASSETS_PATH = os.path.join(os.path.dirname(__file__), str(config["assets"]["assets_path"]))

class Game(arcade.Window):
    """
        Main app class
    """    

    def __init__(self, game_grid = [
            ["0", "0", " ", " ", " ", "0", "0"],
            ["0", "0", " ", " ", " ", "0", "0"],
            [" ", " ", "F", " ", "F", " ", " "],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["0", "0", "C", "C", "C", "0", "0"],
            ["0", "0", "C", "C", "C", "0", "0"]
        ]):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chickens VS Fox")
        arcade.set_background_color(arcade.csscolor.WHITE)

        # size sprite 
        self.target_width = 90
        self.target_height = 90

        # load assets
        self.chicken_texture_path = os.path.join(ASSETS_PATH, "chickens/chicken_.png")
        self.fox_texture_path = os.path.join(ASSETS_PATH, "foxes/fox_.png")
        self.plant_texture_path = os.path.join(ASSETS_PATH, "plants/plant_.png")
        self.grass_texture_path = os.path.join(ASSETS_PATH, "plants/grass_.png")

        # List for obj in grid
        self.chickens = []
        self.foxes = []
        self.plants = []

        # init selected chicken
        self.selected_chicken = None

        # create obj
        self._create_obj(game_grid)

        # Who step ?
        self.turn = "chicken"  

        # Where can go ?
        # _possible_cell_step - list
        # info for list: [ [cell, isFree], [cell, isFree]   ...]
        #       cell - map (x_grid, y_grid)
        #       isFree - bool
        self._possible_cell_step = None

    def _create_obj(self, game_grid):
        # create obj in game grid
        for row in range(len(game_grid)):
            for col in range(len(game_grid[row])):
                if game_grid[row][col] == "C":
                    chicken = Chicken(col * CELL_SIZE + CELL_SIZE / 2 + LEFT_EDGE_GRID, row * CELL_SIZE + CELL_SIZE / 2, self.chicken_texture_path)
                    self.chickens.append(chicken)
                elif game_grid[row][col] == "F":
                    fox = Fox(col * CELL_SIZE + CELL_SIZE / 2 + LEFT_EDGE_GRID, row * CELL_SIZE + CELL_SIZE / 2, self.fox_texture_path)
                    self.foxes.append(fox)
                elif game_grid[row][col] == "0":
                    plant = Plant(col * CELL_SIZE + CELL_SIZE / 2 + LEFT_EDGE_GRID, row * CELL_SIZE + CELL_SIZE / 2, self.plant_texture_path)
                    self.plants.append(plant)
        
    def setup(self):
        """Set up the game."""

    def on_draw(self):
        """Render the screen"""
        # Clear screen
        arcade.start_render()



        #self.draw_info()
        self.draw_grid()

        # paint obj
        for chicken in self.chickens:
            chicken.draw()
        for fox in self.foxes:
            fox.draw()
        for plant in self.plants:
            plant.draw()

        if self._possible_cell_step:
            for cell_info in self._possible_cell_step:
                if cell_info[1]:
                    cell_x = cell_info[0][0]*CELL_SIZE+CELL_SIZE/2 + LEFT_EDGE_GRID
                    cell_y = cell_info[0][1]*CELL_SIZE+CELL_SIZE/2
                    arcade.draw_rectangle_outline(cell_x, cell_y, CELL_SIZE, CELL_SIZE, arcade.color.GREEN, 5)

    # Draw wall grid
    def draw_grid(self):
        arcade.draw_texture_rectangle(GRID_SIZE*CELL_SIZE/2 + LEFT_EDGE_GRID, 
                                      GRID_SIZE*CELL_SIZE/2, 
                                      GRID_SIZE*CELL_SIZE, 
                                      GRID_SIZE*CELL_SIZE, 
                                      arcade.load_texture(self.grass_texture_path))

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE + CELL_SIZE/2 + LEFT_EDGE_GRID
                y = row * CELL_SIZE + CELL_SIZE/2
                arcade.draw_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.BLACK)
           
    def on_mouse_press(self, x, y, button, modifiers):
        """Click mouse"""
        col = x // CELL_SIZE - LEFT_EDGE_GRID // CELL_SIZE
        row = y // CELL_SIZE

        # print('X -', col, 'Y -', row)

        # Mouse click on chiken ??
        for chicken in self.chickens:
            if chicken.grid_position == (col, row):
                # print('\n\n', chicken.grid_position)
                 # Toggle selection of the chicken
                if self.selected_chicken == chicken:
                    chicken.on_click()  # Deselect the chicken
                    self.selected_chicken = None
                    self._possible_cell_step = None
                else:
                    if self.selected_chicken:
                        self.selected_chicken.on_click()  # Deselect previously selected chicken
                    chicken.on_click()  # Select the new chicken
                    self.selected_chicken = chicken
                    self._search_possible_step_for_obj_in_gameGrid(self.selected_chicken)

    def on_key_press(self, symbol, modifiers):
        """Handle key presses for moving the selected chicken"""
        if self.selected_chicken:
            x_grid, y_grid = self.selected_chicken.grid_position
            

            if symbol == arcade.key.RIGHT:
                if (x_grid_new := x_grid+1) < GRID_SIZE:
                    self._move_obj(self.selected_chicken, x_grid_new, y_grid)
            elif symbol == arcade.key.LEFT:
                if (x_grid_new := x_grid-1) > -1:
                    self._move_obj(self.selected_chicken, x_grid_new, y_grid)
            elif symbol == arcade.key.UP:
                if (y_grid_new := y_grid+1) < GRID_SIZE:
                    self._move_obj(self.selected_chicken, x_grid, y_grid_new)
            elif symbol == arcade.key.DOWN:
                if (y_grid_new := y_grid-1) > -1:
                    self._move_obj(self.selected_chicken, x_grid, y_grid_new)

            self.on_draw()  

    def _move_obj(self, obj, x_grid_new, y_grid_new):
        if isinstance(obj, Fox):
            obj.move(x_grid_new, y_grid_new)
            self._possible_cell_step = None
            self._search_possible_step_for_obj_in_gameGrid(obj)
        elif isinstance(obj, Chicken):
            for alone_obj in self._full_obj_in_grid:
                if alone_obj.grid_position == (x_grid_new, y_grid_new):
                    return False
            obj.move(x_grid_new, y_grid_new)
            self._possible_cell_step = None
            self._search_possible_step_for_obj_in_gameGrid(obj)

    def _search_possible_step_for_obj_in_gameGrid(self, obj_gameGrid):
        obj_x, obj_y = obj_gameGrid.grid_position
        possible_cells = list()
        if obj_y+1 < GRID_SIZE:
            possible_cells.append((obj_x,obj_y+1))
        if obj_y-1 > -1:
            possible_cells.append((obj_x,obj_y-1))
        if obj_x+1 < GRID_SIZE:
            possible_cells.append((obj_x+1,obj_y))
        if obj_x-1 > -1:
            possible_cells.append((obj_x-1,obj_y))

        self._possible_cell_step = self._is_occupied_cell(possible_cells)
        # print(self._possible_cell_step)

    @property 
    def _full_obj_in_grid(self):
        return self.chickens + self.foxes + self.plants

    def _is_occupied_cell(self, possible_cells):
        """
            return:
                - info_cell_TF - list
                        info one element in list [cell, occupied]
                            - cell = (x, y)
                            - occupied = bool
        """

        info_cell_TF = list()

        for possible_cell in possible_cells:
            info_cell_TF.append([possible_cell, True])

        for obj in self._full_obj_in_grid:
            for cell_indx in range(len(info_cell_TF)):
                if obj.grid_position == info_cell_TF[cell_indx][0]:
                    info_cell_TF[cell_indx][1] = False

        return info_cell_TF

    def switch_turn(self):
        """Switch between chicken and fox turns"""
        if self.turn == "chicken":
            self.turn = "fox"
        else:
            self.turn = "chicken"

    # self.on_draw()
    def update(self, delta_time):
        """ Update sprite """
        pass

    # def draw_info(self):
    #     """ Info table right"""
    #     # Задаем размеры и позицию панели
    #     panel_width = 300
    #     panel_x = SCREEN_WIDTH - panel_width // 2 + 20
    #     panel_y = SCREEN_HEIGHT // 2

    #     # Рисуем фон панели
    #     arcade.draw_lrtb_rectangle_filled(SCREEN_WIDTH - panel_width, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.LIGHT_GREEN)

    #     # Текстовые данные
    #     #total_chickens = sum(row.count("C") for row in self.game_grid)
    #     #total_foxes = sum(row.count("F") for row in self.game_grid)

    #     # Заголовок
    #     arcade.draw_text("Информация о игре", panel_x - 160, SCREEN_HEIGHT - 50, arcade.color.BLACK, 20)

    #     # Ход игры
    #     #arcade.draw_text(f"Ход: {'Кур' if self.turn == 'chicken' else 'Лис'}", panel_x - 160, SCREEN_HEIGHT - 100, arcade.color.BLACK, 18)


    #     if self.selected_chicken:
    #         # Выбрана курица 
    #         x, y = self.selected_chicken.grid_position
    #         arcade.draw_text(f"X: {x} Y: {y}", panel_x - 160, SCREEN_HEIGHT - 100, arcade.color.BLACK, 18)
    #     else:
    #         arcade.draw_text(f"No select", panel_x - 160, SCREEN_HEIGHT - 100, arcade.color.BLACK, 18)

    #     # Количество кур и лис
    #     arcade.draw_text(f"Кур на поле: {len(self.chickens)}", panel_x - 160, SCREEN_HEIGHT - 150, arcade.color.BLACK, 18)
    #     arcade.draw_text(f"Лис на поле: {len(self.foxes)}", panel_x - 160, SCREEN_HEIGHT - 200, arcade.color.BLACK, 18)

    #     # Отображаем, чья очередь
    #     arcade.draw_text(f"Текущий ход: {'Курицы' if self.turn == 'chicken' else 'Лисы'}", panel_x - 160, SCREEN_HEIGHT - 250, arcade.color.BLACK, 18)















def main():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    main()