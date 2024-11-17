import arcade
from tools import config, Button, AnimatedBackground
from gameView import GameView

# SCREEN
SCREEN_WIDTH = int(config["general"]["screen_width"])
SCREEN_HEIGHT =  int(config["general"]["screen_height"])

background_color = (int(config["color scheme"]["background_color_r"]), 
                    int(config["color scheme"]["background_color_g"]),
                    int(config["color scheme"]["background_color_b"]))  
text_color = (int(config["color scheme"]["text_color_r"]),
              int(config["color scheme"]["text_color_g"]),
              int(config["color scheme"]["text_color_b"])) 
button_color = (int(config["color scheme"]["button_color_r"]),
                int(config["color scheme"]["button_color_g"]),
                int(config["color scheme"]["button_color_b"]))

class Menu_View(arcade.View):
    """ Main menu """

    def __init__(self):
        super().__init__()
        self.bg = AnimatedBackground("assets\\menuView\\background", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._buttons = self._create_buttons()

    def _create_buttons(self):
        buttons = []

        button_height = 200
        button_width = 300 
        button_indention = 100

        # Exit app
        buttons.append(Button(SCREEN_WIDTH // 2, button_indention * len(buttons), 
                              button_width, button_height, 'Exit',
                              'assets/menuView/button/down_button/folder-1.png', 
                              'assets/menuView/button/down_button/folder-1.png', 
                               self._quit_game))

        # Info Game
        buttons.append(Button(SCREEN_WIDTH // 2, button_indention * len(buttons),
                              button_width, button_height, 'Info', 
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-1.png', 
                              None))
        
        # Leader boart
        buttons.append(Button(SCREEN_WIDTH // 2, button_indention * len(buttons),
                              button_width, button_height, 'Leader Boart',
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-1.png', 
                              None))
        

        # Start Game
        buttons.append(Button(SCREEN_WIDTH // 2, button_indention * len(buttons) + 100,
                              button_width, button_height, 'Start Game',
                              "assets/menuView/button/UP_button/folder-1.png",
                              "assets/menuView/button/UP_button/folder-1.png", self._start_game))

        return buttons
    
    def on_mouse_motion(self, x, y, dx, dy):
        for button in self._buttons:
            button.check_hover(x,y)


    def on_draw(self):
        arcade.start_render()
        # background
        self.bg.draw()
        arcade.draw_text("Welcome to Chickens vs Fox", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, arcade.color.BLACK, 24)
        for button in self._buttons:
            button.on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self._buttons:
            button.check_click(x, y)

    def update(self, delta_time):
        self.bg.update() 

    def _start_game(self):
        gameView = GameView(self)
        self.window.show_view(gameView)

    def _quit_game(self):
        self.window.close()
