import arcade
from tools import config, Button, AnimatedBackground, BlinkingText, RulesView
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

    def __init__(self, window):
        super().__init__(window)
        self.bg = AnimatedBackground("assets/menuView/background", 
                                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)               
        self._buttons = self._create_buttons_and_title()

    def _create_buttons_and_title(self):
        
        self._title = BlinkingText("Chickens VS Foxes", 
                                    SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.1, 100)      

        buttons = []

        button_height = 100
        button_width = 300 
        button_indention = 100
        button_exit_with = 150

        # Exit app
        buttons.append(Button(SCREEN_WIDTH // 2, 150, 
                              button_width, button_height, 'Exit',
                              'assets/menuView/button/exit_button/folder-2.png', 
                              'assets/menuView/button/exit_button/folder-4.png', 
                               self.quit_game))

        # Info Game
        buttons.append(Button(SCREEN_WIDTH // 2, button_exit_with + button_indention * len(buttons),
                              button_width, button_height, 'Info', 
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-2.png', 
                              self.show_rules))
        
        # Leader boart
        buttons.append(Button(SCREEN_WIDTH // 2, button_exit_with + button_indention * len(buttons),
                              button_width, button_height, 'Leader Boart',
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-2.png', 
                              None)) 

        # Start Game
        buttons.append(Button(SCREEN_WIDTH // 2, button_exit_with + button_indention * len(buttons),
                              button_width, button_height, 'Start Game',
                              "assets/menuView/button/start_button/folder-1.png",
                              "assets/menuView/button/start_button/folder-2.png", self.start_game))

        return buttons
    
    def on_mouse_motion(self, x, y, dx, dy):
        for button in self._buttons:
            button.check_hover(x,y)

    def on_draw(self):
        arcade.start_render()
        # background
        self.bg.draw()
        self._title.draw()

        arcade.draw_text("Main menu",
                    SCREEN_WIDTH // 2 + 2, int(SCREEN_HEIGHT - SCREEN_HEIGHT * 0.3) - 3,
                    arcade.color.BLACK, 61, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        arcade.draw_text("Main menu",
                    SCREEN_WIDTH // 2, int(SCREEN_HEIGHT - SCREEN_HEIGHT * 0.3),
                    arcade.color.WHITE, 60, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')
 

        for button in self._buttons:
            button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self._buttons:
            button.check_click(x, y)

    def update(self, delta_time):
        self.bg.update() 
        self._title.update(delta_time)

    def start_game(self):
        gameView = GameView(self)
        self.window.show_view(gameView)

    def quit_game(self):
        self.window.close()

    def show_rules(self):
        rules_view = RulesView(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.previous_view = self 
        self.window.show_view(rules_view)
