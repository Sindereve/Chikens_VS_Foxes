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

        self._button_board = self._create_button_board()

        self._info_board = InfoBoard(SCREEN_WIDTH - 150, int(SCREEN_HEIGHT//2 - SCREEN_HEIGHT*0.1), 
                                        200, int(SCREEN_HEIGHT - SCREEN_HEIGHT*0.2), 20, 2, 0, 'Chickens')

        print(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT - SCREEN_HEIGHT * 0.05))
        self.game_grid = GameGrid()

    def _create_button_board(self):
        my_functional = [self._go_last_view]
        button_board = ButtonBoard(150, int(SCREEN_HEIGHT//2 - SCREEN_HEIGHT*0.1), 
                                        200, int(SCREEN_HEIGHT - SCREEN_HEIGHT*0.2), my_functional)
        return button_board
    
    def _go_last_view(self):
        print('--Exit work-- in View')
        self.window.show_view(self.__last_view)


    def on_draw(self):
        arcade.start_render()
        self.bg.draw()
        self._info_board.draw()
        self._button_board.draw()
        self._draw_title()
        self.game_grid.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self._button_board.on_mouse_motion(x, y, dx, dy)

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
        "Click mouse"
        self.game_grid.on_mouse_press(x, y)
        self._button_board.check_click(x, y)
        # self._button_board.on_mouse_press(x, y)

    def on_key_press(self, symbol, modifiers):
        """Click key"""

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.__last_view)
        else:
            self.game_grid.on_key_press(symbol, modifiers)
            self._info_board.update_info(self.game_grid.count_chicken,
                                         self.game_grid.count_fox,
                                         self.game_grid.number_step,
                                         self.game_grid.who_step)


    def update(self, delta_time):
        self.bg.update()

        