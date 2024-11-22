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
            [" ", " ", "F", " ", "F", " ", " "],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["0", "0", "C", "C", "C", "0", "0"],
            ["0", "0", "C", "C", "C", "0", "0"]
        ]):
        
        # size sprite 
        self.target_width = 90
        self.target_height = 90

        # route_fox
        self._route_fox = []
        self._fox_mega_kill = None

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
        self._number_step = 0

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
            # elif symbol == arcade.key.UP:
            #     if (y_grid_new := y_grid+1) < GRID_SIZE:
            #         self._move_obj(self._selected_chicken, x_grid, y_grid_new)
            elif symbol == arcade.key.DOWN:
                if (y_grid_new := y_grid-1) > -1:
                    self._move_obj(self._selected_chicken, x_grid, y_grid_new)

    def _move_obj(self, obj, x_grid_new = 0, y_grid_new = 0, list_move_position = []):
        if isinstance(obj, Fox):
            if list_move_position:
                list_del_obj_pos = []
                list_move_position.pop(0)
                for move_position in list_move_position:
                    x_fact, y_fact = obj.grid_position 
                    x_del, y_del = x_fact, y_fact 
                    if x_fact != move_position[0]:
                        x_del-=(x_fact-move_position[0])//2
                    elif y_fact != move_position[1]:
                        y_del-=(y_fact-move_position[1])//2
                    
                    
                    self._del_obj_for_pos((x_del, y_del))
                    list_del_obj_pos.append((x_del, y_del))
                    obj.move(move_position[0], move_position[1])
            else:
                
                obj.move(x_grid_new, y_grid_new)
                self._possible_cell_step = None
        elif isinstance(obj, Chicken):
            for alone_obj in self._full_obj_in_grid:
                if alone_obj.grid_position == (x_grid_new, y_grid_new):
                    return False
            obj.move(x_grid_new, y_grid_new)
            self._possible_cell_step = None
            self._auto_eat_and_move_fox()

            if self._selected_chicken:
                self._selected_chicken.on_click()
                self._selected_chicken = None
            
       
    def _auto_eat_and_move_fox(self):
        self._number_step+=1
        self._switch_turn()
        self._route_fox = []
        self._fox_mega_kill = None
        info_do_foxs = []
        
        for fox in self._foxes:
            info_do_foxs.append(self._search_possible_step_for_obj_in_gameGrid(fox))

        is_eat = False
        if self._fox_mega_kill:
            print('MEGA KILL')
            is_eat = True
            self._move_obj(self._fox_mega_kill, list_move_position=self._route_fox)
        else:
            for info_do_fox in info_do_foxs:
                obj = info_do_fox[0]
                status = info_do_fox[1]
                if status == ' Fox eat ':
                    print(status)
                    is_eat = True
                    grid_pos = info_do_fox[2][0][0]
                    self._move_obj(info_do_fox[0], list_move_position=[grid_pos,grid_pos])
                    self._switch_turn()
                    break
        if is_eat == False:
            self._random_step_fox_no_eat(info_do_foxs)
            

    def _random_step_fox_no_eat(self, info_do_foxs):
        number_fox = randint(0, len(self._foxes)-1)
        for info_fox in info_do_foxs:
            print(info_fox)
        
        for info_do_fox in info_do_foxs:
            if info_do_fox[0] == self._foxes[number_fox]:
                info_step = info_do_fox[2]
                if len(info_step) > 0:
                    number_step = randint(0, len(info_step)-1)
                    x, y = info_step[number_step][0][0], info_step[number_step][0][1]
                    self._move_obj(self._foxes[number_fox] , x, y)
                    self._switch_turn()
                    break
                else:
                    self._random_step_fox_no_eat( info_do_foxs)


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

            is_eat = ' Fox NO eat '

            for cell in is_occupied_cell:
                if cell[2] == 'eating':
                    # новая позиция для лисы
                    new_pos = (cell[0][0], cell[0][1])
                    

                    # лиса может сьесть курицу
                    is_eat = ' Fox eat '

                    mb = self._create_list_possible_step(obj_gameGrid ,cell[0][0], cell[0][1], [obj_gameGrid.grid_position])

                    count = self._is_occupied_cell(mb,                                                                      # ищем возможные клетки
                                                obj_gameGrid, new_pos,                                              # передаём обьект и кординаты
                                                history_last_step= [obj_gameGrid.grid_position, new_pos])            # передаём историю, где был обьект
                
            return (obj_gameGrid, is_eat, possible_cells_history)
        elif isinstance(obj_gameGrid, Chicken):

            obj_x, obj_y = obj_gameGrid.grid_position
            possible_cells = self._create_list_possible_step(obj_gameGrid, obj_x, obj_y)

            return self._is_occupied_cell(possible_cells, obj_gameGrid)

    def _create_list_possible_step(self, select_obj, obj_x, obj_y, ceels_hist = []):
        if isinstance(select_obj, Fox):
            possible_cells = list()

            possible_cells.append((obj_x,obj_y+2))
            possible_cells.append((obj_x,obj_y+1))

            possible_cells.append((obj_x,obj_y-2))
            possible_cells.append((obj_x,obj_y-1))

            possible_cells.append((obj_x+2,obj_y))
            possible_cells.append((obj_x+1,obj_y))

            possible_cells.append((obj_x-2,obj_y))
            possible_cells.append((obj_x-1,obj_y))


            numbers_del = []
            for cell_indx in range(len(possible_cells)):
                if possible_cells[cell_indx] in ceels_hist:
                    numbers_del.append(cell_indx)
                    numbers_del.append(cell_indx+1)
            for indx in range(len(numbers_del)-1,-1,-1):
                possible_cells.pop(numbers_del[indx])
        
            return possible_cells
        
        if isinstance(select_obj, Chicken):
            possible_cells = list()

            if obj_y-1 > -1:
                possible_cells.append((obj_x,obj_y-1))
            if obj_x+1 < GRID_SIZE:
                possible_cells.append((obj_x+1,obj_y))
            if obj_x-1 > -1:
                possible_cells.append((obj_x-1,obj_y))

            return possible_cells

    def _is_occupied_cell(self, possible_cells, select_obj, grid_pos_for_eating = None, history_last_step = []):
        """
            return:
                - info_cell_TF - list
                        info one element in list [cell, occupied]
                            - cell = (x, y)
                            - occupied = bool
                            - modification = str
        """
        if isinstance(select_obj, Fox):
            if grid_pos_for_eating == None:

                info_cell_TF = list()
                
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

                for indx in range(len(new_list_is_occupied_cell)-1,-1,-1):
                    if new_list_is_occupied_cell[indx][0][0] < 0 or new_list_is_occupied_cell[indx][0][0] >= GRID_SIZE:
                        new_list_is_occupied_cell.pop(indx)
                    elif new_list_is_occupied_cell[indx][0][1] < 0 or new_list_is_occupied_cell[indx][0][1] >= GRID_SIZE:
                        new_list_is_occupied_cell.pop(indx)


                eat_is_occupied_cell = []
                for is_occupied_cell in new_list_is_occupied_cell:
                    if is_occupied_cell[2] == 'eating':
                        eat_is_occupied_cell.append(is_occupied_cell)
                
                if not len(eat_is_occupied_cell):
                    eat_is_occupied_cell = new_list_is_occupied_cell

                return eat_is_occupied_cell
            else:

                # информация о каждой клетке, +2 от наших кординат
                info_cell_TF = list()

                for possible_cell in possible_cells:
                    info_cell_TF.append([possible_cell, True, None])

                for obj in self._full_obj_in_grid:
                    for cell_indx in range(len(info_cell_TF)):
                        if obj.grid_position == info_cell_TF[cell_indx][0]:
                            info_cell_TF[cell_indx][1] = False
                            info_cell_TF[cell_indx][2] = obj.typeOb
                
                # список отфильтрованных клеток (нету занятых клеток, проходит проверка на возможность сьесть)
                new_list_is_occupied_cell = []

                for indx in range(0, len(info_cell_TF), 2):
                    if info_cell_TF[indx+1][1]:
                        new_list_is_occupied_cell.append(info_cell_TF[indx+1])
                    else:
                        if info_cell_TF[indx][1] and info_cell_TF[indx+1][2] == 'Chicken':
                            new_list_is_occupied_cell.append(info_cell_TF[indx])
                            new_list_is_occupied_cell[-1][2] = 'eating'


                for indx in range(len(new_list_is_occupied_cell)-1,-1,-1):
                    if new_list_is_occupied_cell[indx][0][0] < 0 or new_list_is_occupied_cell[indx][0][0] >= GRID_SIZE:
                        new_list_is_occupied_cell.pop(indx)
                    elif new_list_is_occupied_cell[indx][0][1] < 0 or new_list_is_occupied_cell[indx][0][1] >= GRID_SIZE:
                        new_list_is_occupied_cell.pop(indx)

                # сохраняем только клетки с модификатором eating и которых не было в истории
                eat_is_occupied_cell = []
                for is_occupied_cell in new_list_is_occupied_cell:
                    if is_occupied_cell[2] == 'eating':
                        for history_one_step in history_last_step:
                            if is_occupied_cell[0] != history_one_step:
                                if is_occupied_cell not in eat_is_occupied_cell:
                                    eat_is_occupied_cell.append(is_occupied_cell)


                result = []
                res = []

                # если у нас есть клетки с модификатором eat, то мы сохраняем только их, т.к. лисы обязаны есть куриц
                if not len(eat_is_occupied_cell):
                    eat_is_occupied_cell = new_list_is_occupied_cell
                else:
                    # если есть клетки с модификатором, перебираем их и ищем самый большой из алгоритмов

                    for cell in eat_is_occupied_cell:
                        if (cell[0][0], cell[0][1]) not in history_last_step:
                            copy = history_last_step.copy()
                            copy.append((cell[0][0], cell[0][1]))


                            cells = self._create_list_possible_step(select_obj, cell[0][0], cell[0][1])
                            
                            self._is_occupied_cell(cells, select_obj, (cell[0][0], cell[0][1]), copy)
                            
                            if len(copy) > len(self._route_fox):
                                self._fox_mega_kill = select_obj
                                self._route_fox = copy

                # выводим клетки на которые мы можем ходить
                return history_last_step

        elif isinstance(select_obj, Chicken):

            info_cell_TF = list()

            for possible_cell in possible_cells:
                info_cell_TF.append([possible_cell, True, None])

            for obj in self._full_obj_in_grid:
                for cell_indx in range(len(info_cell_TF)):
                    if obj.grid_position == info_cell_TF[cell_indx][0]:
                        info_cell_TF[cell_indx][1] = False
                        info_cell_TF[cell_indx][2] = type(obj)

            return info_cell_TF

    def _switch_turn(self):
        """Switch between chicken and fox turns"""
        if self._turn == "chicken":
            self._turn = "fox"
        else:
            self._turn = "chicken"
    
    @property
    def win_or_loos(self):
        '''
            return 'loss'/'win'/'game is working'
        '''
        counte_chiken_in_win_possition = 0 
        for chiken in self._chickens:
            if chiken.grid_position[1] < 3 and chiken.grid_position[0] > 1 and chiken.grid_position[0] < 5:
                counte_chiken_in_win_possition += 1

        if self.count_chicken < 9:
            return 'loss'
        elif counte_chiken_in_win_possition > 8:
            return 'win'
        return 'game is working'

    @property
    def count_chicken(self):
        return len(self._chickens)

    @property
    def count_fox(self):
        return len(self._foxes)

    @property
    def number_step(self):
        return self._number_step

    @property
    def who_step(self):
        return self._turn