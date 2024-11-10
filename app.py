import arcade
import arcade.csscolor
import arcade.csscolor

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Chiken VS Fox"

GRID_SIZE = 7
CELL_SIZE = 100

CHARACTER_SCALING = 1
TILE_SCALING = 0.5

class Game(arcade.Window):
    """
        Main app class
    """    

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # init game grid
        self.game_grid = None

        # init selectid chiken
        self.selected_chicken = None

        # Кто ходит: "chicken" или "fox"
        self.turn = "chicken"  

        arcade.set_background_color(arcade.csscolor.GREY)
    
    def setup(self):
        """Set up the game."""

        # Init grid
        self.game_grid = [
            ["0", "0", " ", " ", " ", "0", "0"],
            ["0", "0", " ", " ", " ", "0", "0"],
            [" ", " ", "F", " ", "F", " ", " "],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C"],
            ["0", "0", "C", "C", "C", "0", "0"],
            ["0", "0", "C", "C", "C", "0", "0"]
        ]
        
        self.chiken_texture = arcade.load_texture("images/sprites/chikens/chiken_.png")
        self.fox_texture = arcade.load_texture("images/sprites/foxs/fox_.png")
        self.plant_texture = arcade.load_texture("images/sprites/plants/plant_.png")
        self.grass_texture = arcade.load_texture("images/sprites/plants/grass_.png")

    
    def on_draw(self):
        """Render the screen"""
        # Clear screen
        self.clear()
        self.draw_info()
        self.draw_grid()
        



    # Draw wall grid
    def draw_grid(self):
        arcade.draw_texture_rectangle(GRID_SIZE*CELL_SIZE/2, GRID_SIZE*CELL_SIZE/2, GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE, self.grass_texture)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE + CELL_SIZE/2
                y = row * CELL_SIZE + CELL_SIZE/2
                arcade.draw_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.BLACK)

                if self.game_grid[row][col] == "C":
                    arcade.draw_texture_rectangle(x, y, CELL_SIZE, CELL_SIZE, self.chiken_texture)
                elif self.game_grid[row][col] == "F":
                    arcade.draw_texture_rectangle(x, y, CELL_SIZE, CELL_SIZE, self.fox_texture)
                elif self.game_grid[row][col] == "0":
                    arcade.draw_texture_rectangle(x, y, CELL_SIZE, CELL_SIZE, self.plant_texture)
        
        if self.selected_chicken:
            row, col = self.selected_chicken
            x = col * CELL_SIZE + CELL_SIZE / 2
            y = row * CELL_SIZE + CELL_SIZE / 2
            arcade.draw_rectangle_outline(x, y, CELL_SIZE, CELL_SIZE, arcade.color.RED, 5)

                
    def on_mouse_press(self, x, y, button, modifiers):
        """Click mouse"""
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        # Mouse click on chiken ??
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            if self.game_grid[row][col] == "C":
                # It is last chiken
                if self.selected_chicken == (row, col):
                    self.selected_chicken = None
                else:
                    # Selected chiken
                    self.selected_chicken = (row, col)
            else:
                self.selected_chicken = None

    def on_key_press(self, symbol, modifiers):
        """Обрабатывает нажатия клавиш для перемещения выбранной курицы"""
        if self.selected_chicken:
            row, col = self.selected_chicken

            # Chiken step 
            if symbol == arcade.key.RIGHT:
                if col + 1 < GRID_SIZE and self.game_grid[row][col + 1] == " ":
                    self.game_grid[row][col] = " "
                    self.game_grid[row][col + 1] = "C"
                    self.selected_chicken = (row, col + 1)
            elif symbol == arcade.key.LEFT:
                if col - 1 >= 0 and self.game_grid[row][col - 1] == " ":
                    self.game_grid[row][col] = " "
                    self.game_grid[row][col - 1] = "C"
                    self.selected_chicken = (row, col - 1)
            elif symbol == arcade.key.UP:
                if row + 1 < GRID_SIZE and self.game_grid[row + 1][col] == " ":
                    self.game_grid[row][col] = " "
                    self.game_grid[row + 1][col] = "C"
                    self.selected_chicken = (row + 1, col)
            elif symbol == arcade.key.DOWN:
                if row - 1 >= 0 and self.game_grid[row - 1][col] == " ":
                    self.game_grid[row][col] = " "
                    self.game_grid[row - 1][col] = "C"
                    self.selected_chicken = (row - 1, col)

            self.on_draw()

        

    def draw_info(self):
        """ Info table right"""
        # Задаем размеры и позицию панели
        panel_width = 300
        panel_x = SCREEN_WIDTH - panel_width // 2 + 20
        panel_y = SCREEN_HEIGHT // 2

        # Рисуем фон панели
        arcade.draw_lrtb_rectangle_filled(SCREEN_WIDTH - panel_width, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.LIGHT_GREEN)

        # Текстовые данные
        total_chickens = sum(row.count("C") for row in self.game_grid)
        total_foxes = sum(row.count("F") for row in self.game_grid)

        # Заголовок
        arcade.draw_text("Информация о игре", panel_x - 160, SCREEN_HEIGHT - 50, arcade.color.BLACK, 20)

        # Ход игры
        arcade.draw_text(f"Ход: {'Кур' if self.turn == 'chicken' else 'Лис'}", panel_x - 160, SCREEN_HEIGHT - 100, arcade.color.BLACK, 18)

        # Количество кур и лис
        arcade.draw_text(f"Кур на поле: {total_chickens}", panel_x - 160, SCREEN_HEIGHT - 150, arcade.color.BLACK, 18)
        arcade.draw_text(f"Лис на поле: {total_foxes}", panel_x - 160, SCREEN_HEIGHT - 200, arcade.color.BLACK, 18)

        # Отображаем, чья очередь
        arcade.draw_text(f"Текущий ход: {'Курицы' if self.turn == 'chicken' else 'Лисы'}", panel_x - 160, SCREEN_HEIGHT - 250, arcade.color.BLACK, 18)

        



                
                    




def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()