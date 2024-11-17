import arcade
from tools import config, AnimatedBackground, InfoBoard, ButtonBoard
from gameGrid import GameGrid

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

class GameView(arcade.View):

    def __init__(self, last_view):
        super().__init__()
         
        self.__last_view = last_view
        self.bg = AnimatedBackground("assets/gameView/background", 
                                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                                        SCREEN_WIDTH, SCREEN_HEIGHT)
        self._info_board = InfoBoard(SCREEN_WIDTH - 150, int(SCREEN_HEIGHT//2 - SCREEN_HEIGHT*0.1), 
                                        200, int(SCREEN_HEIGHT - SCREEN_HEIGHT*0.2), 20, 2, 0, 'Chickens')

        self._button_board = ButtonBoard(150, int(SCREEN_HEIGHT//2 - SCREEN_HEIGHT*0.1), 
                                        200, int(SCREEN_HEIGHT - SCREEN_HEIGHT*0.2))

        print(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT - SCREEN_HEIGHT * 0.05))
        self.game_grid = GameGrid()

    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self._info_board.draw()
        self._button_board.draw()
        self._draw_title()
        self.game_grid.draw()

    def _draw_title(self):
        text = "Chickens VS Foxes" 
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT - SCREEN_HEIGHT * 0.1
        font_size = 100

        arcade.draw_text(text, x + 3, y - 3, 
                    arcade.color.BLACK, font_size , font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        arcade.draw_text(text , x, y, (255, 0, 0), 
                    font_size, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов мыши в игре"""
        self.game_grid.on_mouse_press(x, y)

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатий клавиш в игре"""

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.__last_view)
        else:
            self.game_grid.on_key_press(symbol, modifiers)       

    def update(self, delta_time):
        self.bg.update()
        