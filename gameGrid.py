import arcade
from tools import load_config
from random import randint
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

class GameGrid:
    def __init__(self, game_grid = [
            ["0", "0", " ", " ", " ", "0", "0"],
            ["0", "0", " ", " ", " ", "0", "0"],
            [" ", " ", " ", " ", "F", " ", " "],
            ["C", "C", "C", "C", "C", "C", "C"],
            [" ", "C", " ", "C", " ", "C", "C"],
            ["0", "0", "C", "C", "C", "0", "0"],
            ["0", "0", " ", "C", "C", "0", "0"]
        ]):
        
        # size sprite 
        self.target_width = 90
        self.target_height = 90

        # load assets
        self.chicken_texture_path = os.path.join(ASSETS_PATH, "chickens/chicken_.png")
        self.fox_texture_path = os.path.join(ASSETS_PATH, "foxes/fox_.png")
        self.plant_texture_path = os.path.join(ASSETS_PATH, "plants/plant_.png")
        self.grass_texture_path = os.path.join(ASSETS_PATH, "plants/grass_.png")

        # List for obj in grid
        self._chickens = []
        self._foxes = []
        self._plants = []

        # init selected chicken
        self._selected_chicken = None

        # create obj
        self._create_obj(game_grid)

        # Who step ?
        self._turn = "chicken"  

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
                    self._chickens.append(chicken)
                elif game_grid[row][col] == "F":
                    fox = Fox(col * CELL_SIZE + CELL_SIZE / 2 + LEFT_EDGE_GRID, row * CELL_SIZE + CELL_SIZE / 2, self.fox_texture_path)
                    self._foxes.append(fox)
                elif game_grid[row][col] == "0":
                    plant = Plant(col * CELL_SIZE + CELL_SIZE / 2 + LEFT_EDGE_GRID, row * CELL_SIZE + CELL_SIZE / 2, self.plant_texture_path)
                    self._plants.append(plant)    

    def draw(self):
        """ Grid draw =) """
        self.draw_grid()

        # paint obj
        for chicken in self._chickens:
            chicken.draw()
        for fox in self._foxes:
            fox.draw()
        for plant in self._plants:
            plant.draw()

        if self._possible_cell_step:
            for cell_info in self._possible_cell_step:
                if cell_info[1]:
                    print(cell_info[1])
                    print(cell_info[0][0])
                    print(cell_info[0][1])
                    cell_x = cell_info[0][0]*CELL_SIZE+CELL_SIZE//2 + LEFT_EDGE_GRID
                    cell_y = cell_info[0][1]*CELL_SIZE+CELL_SIZE//2
                    arcade.draw_rectangle_outline(cell_x, cell_y, CELL_SIZE, CELL_SIZE, arcade.color.GREEN, 5)

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

    def on_mouse_press(self, x, y):
        """Click mouse"""
        col = x // CELL_SIZE - LEFT_EDGE_GRID // CELL_SIZE
        row = y // CELL_SIZE

        # Mouse click on chiken ??
        for chicken in self._chickens:
            if chicken.grid_position == (col, row):
                # print('\n\n', chicken.grid_position)
                 # Toggle selection of the chicken
                if self._selected_chicken == chicken:
                    chicken.on_click()  # Deselect the chicken
                    self._selected_chicken = None
                    self._possible_cell_step = None
                else:
                    if self._selected_chicken:
                        self._selected_chicken.on_click()  # Deselect previously selected chicken
                    chicken.on_click()  # Select the new chicken
                    self._selected_chicken = chicken
                    self._possible_cell_step = self._search_possible_step_for_obj_in_gameGrid(self._selected_chicken)

    @property 
    def _full_obj_in_grid(self):
        return self._chickens + self._foxes + self._plants
    
    def on_key_press(self, symbol, modifiers):
        """Handle key presses for moving the selected chicken"""
        if self._selected_chicken:
            x_grid, y_grid = self._selected_chicken.grid_position
            

            if symbol == arcade.key.RIGHT:
                if (x_grid_new := x_grid+1) < GRID_SIZE:
                    self._move_obj(self._selected_chicken, x_grid_new, y_grid)
            elif symbol == arcade.key.LEFT:
                if (x_grid_new := x_grid-1) > -1:
                    self._move_obj(self._selected_chicken, x_grid_new, y_grid)
            elif symbol == arcade.key.UP:
                if (y_grid_new := y_grid+1) < GRID_SIZE:
                    self._move_obj(self._selected_chicken, x_grid, y_grid_new)
            elif symbol == arcade.key.DOWN:
                if (y_grid_new := y_grid-1) > -1:
                    self._move_obj(self._selected_chicken, x_grid, y_grid_new)

    def _move_obj(self, obj, x_grid_new, y_grid_new):
        if isinstance(obj, Fox):
            obj.move(x_grid_new, y_grid_new)
            self._possible_cell_step = None
            #self._search_possible_step_for_obj_in_gameGrid(obj)

        elif isinstance(obj, Chicken):
            for alone_obj in self._full_obj_in_grid:
                if alone_obj.grid_position == (x_grid_new, y_grid_new):
                    return False
            obj.move(x_grid_new, y_grid_new)
            self._possible_cell_step = None
            
            self._auto_eat_and_move_fox()

            #if not is_eat:
                #self._not_eat_move_fox()    
                #self._possible_cell_step = self._search_possible_step_for_obj_in_gameGrid(obj)
       
    def _auto_eat_and_move_fox(self):
        # indx_fox = randint(0,1)
        # fox = self._foxes[indx_fox]

        print('\n _auto_eat_and_move_fox wok')
        count = 0
        for fox in self._foxes:
            count+=1
            print(' Fox: ', count)
            self._search_possible_step_for_obj_in_gameGrid(fox)
            #print(possible_cell_step)

        #return possible_cell_step

    def _del_obj_for_pos(self, grid_pos):
        
        for indx in range(len(self._chickens)):
            if self._chickens[indx].grid_position == grid_pos:
                if self._chickens[indx] == self._selected_chicken:
                    self._selected_chicken = None
                del self._chickens[indx]
                break

        for indx in range(len(self._foxes)):
            if self._foxes[indx].grid_position == grid_pos:
                del self._foxes[indx]
                break

        for indx in range(len(self._plants)):
            if self._plants[indx].grid_position == grid_pos:
                del self._plants[indx]
                break

    def _not_eat_move_fox(self):
        rand = randint(0,len(self._foxes)-1)
        fox = self._foxes[rand]

        possible_cells_step = self._search_possible_step_for_obj_in_gameGrid(fox)
        cell = possible_cells_step[randint(0,len(possible_cells_step)-1)]
        if not self._is_block_cell(cell[0][0],cell[0][1]):
            fox.move(cell[0][0], cell[0][1])
        else:
            self._not_eat_move_fox()

    def _is_block_cell(self, x, y):
        return y >= GRID_SIZE or y < 0 or x >= GRID_SIZE or x < 0
    
    def _is_chicken_on_cell(self, grid_pos):
        for chiken in self._chickens:
            if chiken.grid_position == grid_pos:
                return True
        return False    
        
    def _search_possible_step_for_obj_in_gameGrid(self, obj_gameGrid):
        if isinstance(obj_gameGrid, Fox):
            obj_x, obj_y = obj_gameGrid.grid_position
        
            possible_cells_history = []
            possible_cells = self._create_list_possible_step(obj_gameGrid, obj_x, obj_y)
            

                # search occupied cell
            is_occupied_cell = self._is_occupied_cell(possible_cells, obj_gameGrid)
            possible_cells_history.extend(is_occupied_cell)
        
            print(possible_cells_history)
            for cell in is_occupied_cell:
                #print(cell[0], cell[1], cell[2])
                if cell[2] == 'eating':
                    grid = (cell[0][0], cell[0][1])

                    n = self._is_occupied_cell(self._create_list_possible_step(obj_gameGrid, cell[0][0], cell[0][1]), obj_gameGrid, grid)
                    print('\nNew step', n)

                    possible_cells_history.extend(possible_cells_history + n)

                
            print(possible_cells_history)
            
            self._possible_cell_step = []
            self._possible_cell_step.extend(p for p in possible_cells_history)                    
            
            return is_occupied_cell
        elif isinstance(obj_gameGrid, Chicken):

            obj_x, obj_y = obj_gameGrid.grid_position
            possible_cells = self._create_list_possible_step(obj_gameGrid, obj_x, obj_y)

            return self._is_occupied_cell(possible_cells, obj_gameGrid)

    def _create_list_possible_step(self, obj_gameGrid, obj_x, obj_y):
        if isinstance(obj_gameGrid, Fox):
            possible_cells = list()

            possible_cells.append((obj_x,obj_y+2))
            possible_cells.append((obj_x,obj_y+1))

            possible_cells.append((obj_x,obj_y-2))
            possible_cells.append((obj_x,obj_y-1))

            possible_cells.append((obj_x+2,obj_y))
            possible_cells.append((obj_x+1,obj_y))

            possible_cells.append((obj_x-2,obj_y))
            possible_cells.append((obj_x-1,obj_y))
            return possible_cells
        
        if isinstance(obj_gameGrid, Chicken):
            possible_cells = list()

            if obj_y-1 > -1:
                possible_cells.append((obj_x,obj_y-1))
            if obj_x+1 < GRID_SIZE:
                possible_cells.append((obj_x+1,obj_y))
            if obj_x-1 > -1:
                possible_cells.append((obj_x-1,obj_y))

            return possible_cells

    def _is_occupied_cell(self, possible_cells, obj, grid_pos_for_eating = None):
        """
            return:
                - info_cell_TF - list
                        info one element in list [cell, occupied]
                            - cell = (x, y)
                            - occupied = bool
                            - modification = str
        """

        if isinstance(obj, Fox):
            info_cell_TF = list()

            if grid_pos_for_eating == None:
                
                for possible_cell in possible_cells:
                    info_cell_TF.append([possible_cell, True, None])

                for obj in self._full_obj_in_grid:
                    for cell_indx in range(len(info_cell_TF)):
                        if obj.grid_position == info_cell_TF[cell_indx][0]:
                            info_cell_TF[cell_indx][1] = False
                            info_cell_TF[cell_indx][2] = obj.typeOb

                new_list_is_occupied_cell = []

                for indx in range(0, len(info_cell_TF), 2):
                    if info_cell_TF[indx+1][1]:
                        new_list_is_occupied_cell.append(info_cell_TF[indx+1])
                    else:
                        if info_cell_TF[indx][1] and info_cell_TF[indx+1][2] == 'Chicken':
                            new_list_is_occupied_cell.append(info_cell_TF[indx])
                            new_list_is_occupied_cell[-1][2] = 'eating'

                eat_is_occupied_cell = []
                for is_occupied_cell in new_list_is_occupied_cell:
                    if is_occupied_cell[2] == 'eating':
                        eat_is_occupied_cell.append(is_occupied_cell)
                
                if not len(eat_is_occupied_cell):
                    eat_is_occupied_cell = new_list_is_occupied_cell

                return eat_is_occupied_cell

            else:

                for possible_cell in possible_cells:
                    info_cell_TF.append([possible_cell, True, None])

                for obj in self._full_obj_in_grid:
                    for cell_indx in range(len(info_cell_TF)):
                        if obj.grid_position == info_cell_TF[cell_indx][0]:
                            info_cell_TF[cell_indx][1] = False
                            info_cell_TF[cell_indx][2] = obj.typeOb

                new_list_is_occupied_cell = []

                for indx in range(0, len(info_cell_TF), 2):
                    if info_cell_TF[indx+1][1]:
                        new_list_is_occupied_cell.append(info_cell_TF[indx+1])
                    else:
                        if info_cell_TF[indx][1] and info_cell_TF[indx+1][2] == 'Chicken':
                            new_list_is_occupied_cell.append(info_cell_TF[indx])
                            new_list_is_occupied_cell[-1][2] = 'eating'

                eat_is_occupied_cell = []
                for is_occupied_cell in new_list_is_occupied_cell:
                    if is_occupied_cell[2] == 'eating':
                        eat_is_occupied_cell.append(is_occupied_cell)
                
                if not len(eat_is_occupied_cell):
                    eat_is_occupied_cell = new_list_is_occupied_cell
                else:
                    for cell in new_list_is_occupied_cell:
                        self._is_occupied_cell(self._create_list_possible_step(obj, cell[0][0], cell[0][1]), obj, (cell[0][0], cell[0][1]))

                return eat_is_occupied_cell
        elif isinstance(obj, Chicken):

            info_cell_TF = list()

            for possible_cell in possible_cells:
                info_cell_TF.append([possible_cell, True, None])

            for obj in self._full_obj_in_grid:
                for cell_indx in range(len(info_cell_TF)):
                    if obj.grid_position == info_cell_TF[cell_indx][0]:
                        info_cell_TF[cell_indx][1] = False
                        info_cell_TF[cell_indx][2] = type(obj)

            return info_cell_TF

    def switch_turn(self):
        """Switch between chicken and fox turns"""
        if self.turn == "chicken":
            self.turn = "fox"
        else:
            self.turn = "chicken"

       

        