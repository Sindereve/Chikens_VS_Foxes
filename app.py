import arcade
from entities import Chicken, Fox, Plant
import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

GRID_SIZE = 7
CELL_SIZE = 100

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

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

        # load assets
        self.chicken_texture_path = os.path.join(ASSETS_PATH, "chickens/chicken_.png")
        self.fox_texture_path = os.path.join(ASSETS_PATH, "foxes/fox_.png")
        self.plant_texture_path = os.path.join(ASSETS_PATH, "plants/plant_.png")
        self.grass_texture_path = os.path.join(ASSETS_PATH, "plants/grass_.png")

        # List for obj in grid
        self.chickens = []
        self.foxes = []
        self.plants = []
        # create obj
        self._create_obj(game_grid)

        # Who step ?
        self.turn = "chicken"  

    def _create_obj(self, game_grid):
        for row in range(len(game_grid)):
            for col in range(len(game_grid[row])):
                if game_grid[row][col] == "C":
                    chicken = Chicken(col * CELL_SIZE + CELL_SIZE / 2, row * CELL_SIZE + CELL_SIZE / 2, self.chicken_texture_path)
                    self.chickens.append(chicken)
                # elif game_grid[row][col] == "F":
                #     fox = Fox(col * CELL_SIZE + CELL_SIZE / 2, rol * CELL_SIZE + CELL_SIZE / 2, self.fox_texture_path)
                #     self.foxes.append(fox)
                elif game_grid[row][col] == "0":
                    plant = Plant(col * CELL_SIZE + CELL_SIZE / 2, row * CELL_SIZE + CELL_SIZE / 2, self.plant_texture_path)
                    self.plants.append(plant)
        
    
    def setup(self):
        """Set up the game."""

        
        

    
    def on_draw(self):
        """Render the screen"""
        # Clear screen
        arcade.start_render()
        
        self.draw_info()
        self.draw_grid()

        for chicken in self.chickens:
            chicken.draw()

        for fox in self.foxes:
            fox.draw()

        # for plant in self.plants:
        #     plant.draw()



    # Draw wall grid
    def draw_grid(self):
        arcade.draw_texture_rectangle(GRID_SIZE*CELL_SIZE/2, GRID_SIZE*CELL_SIZE/2, GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE, arcade.load_texture(self.grass_texture_path))

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE + CELL_SIZE/2
                y = row * CELL_SIZE + CELL_SIZE/2
                arcade.draw_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.BLACK)
        
        # if self.selected_chicken:
        #     row, col = self.selected_chicken
        #     x = col * CELL_SIZE + CELL_SIZE / 2
        #     y = row * CELL_SIZE + CELL_SIZE / 2
        #     arcade.draw_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.RED, 5)

                
    # def on_mouse_press(self, x, y, button, modifiers):
    #     """Click mouse"""
    #     col = x // CELL_SIZE
    #     row = y // CELL_SIZE

    #     # Mouse click on chiken ??
    #     if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
    #         if self.game_grid[row][col] == "C":
    #             # It is last chiken
    #             if self.selected_chicken == (row, col):
    #                 self.selected_chicken = None
    #             else:
    #                 # Selected chiken
    #                 self.selected_chicken = (row, col)
    #         else:
    #             self.selected_chicken = None


    # def on_key_press(self, symbol, modifiers):
    #     """Обрабатывает нажатия клавиш для перемещения выбранной курицы"""
    #     if self.selected_chicken:
    #         row, col = self.selected_chicken

    #         # Chiken step 
    #         if symbol == arcade.key.RIGHT:
    #             if col + 1 < GRID_SIZE and self.game_grid[row][col + 1] == " ":
    #                 self.game_grid[row][col] = " "
    #                 self.game_grid[row][col + 1] = "C"
    #                 self.selected_chicken = (row, col + 1)
    #         elif symbol == arcade.key.LEFT:
    #             if col - 1 >= 0 and self.game_grid[row][col - 1] == " ":
    #                 self.game_grid[row][col] = " "
    #                 self.game_grid[row][col - 1] = "C"
    #                 self.selected_chicken = (row, col - 1)
    #         elif symbol == arcade.key.UP:
    #             if row + 1 < GRID_SIZE and self.game_grid[row + 1][col] == " ":
    #                 self.game_grid[row][col] = " "
    #                 self.game_grid[row + 1][col] = "C"
    #                 self.selected_chicken = (row + 1, col)
    #         elif symbol == arcade.key.DOWN:
    #             if row - 1 >= 0 and self.game_grid[row - 1][col] == " ":
    #                 self.game_grid[row][col] = " "
    #                 self.game_grid[row - 1][col] = "C"
    #                 self.selected_chicken = (row - 1, col)

    #         self.on_draw()

        
    def draw_info(self):
        """ Info table right"""
        # Задаем размеры и позицию панели
        panel_width = 300
        panel_x = SCREEN_WIDTH - panel_width // 2 + 20
        panel_y = SCREEN_HEIGHT // 2

        # Рисуем фон панели
        arcade.draw_lrtb_rectangle_filled(SCREEN_WIDTH - panel_width, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.LIGHT_GREEN)

        # Текстовые данные
        #total_chickens = sum(row.count("C") for row in self.game_grid)
        #total_foxes = sum(row.count("F") for row in self.game_grid)

        # Заголовок
        arcade.draw_text("Информация о игре", panel_x - 160, SCREEN_HEIGHT - 50, arcade.color.BLACK, 20)

        # Ход игры
        arcade.draw_text(f"Ход: {'Кур' if self.turn == 'chicken' else 'Лис'}", panel_x - 160, SCREEN_HEIGHT - 100, arcade.color.BLACK, 18)

        # Количество кур и лис
        #arcade.draw_text(f"Кур на поле: {total_chickens}", panel_x - 160, SCREEN_HEIGHT - 150, arcade.color.BLACK, 18)
        #arcade.draw_text(f"Лис на поле: {total_foxes}", panel_x - 160, SCREEN_HEIGHT - 200, arcade.color.BLACK, 18)

        # Отображаем, чья очередь
        arcade.draw_text(f"Текущий ход: {'Курицы' if self.turn == 'chicken' else 'Лисы'}", panel_x - 160, SCREEN_HEIGHT - 250, arcade.color.BLACK, 18)





def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()