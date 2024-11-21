import arcade
from tools import load_config
from menuView import Menu_View

config = load_config()
# SCREEN
SCREEN_WIDTH = int(config["general"]["screen_width"])
SCREEN_HEIGHT =  int(config["general"]["screen_height"])

class Game(arcade.Window):
    """
        Main app class
    """    

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Chickens VS Fox")
        arcade.set_background_color(arcade.csscolor.WHITE)

        self._menu_view = Menu_View(self)
        self.previous_view = None
        
        self.show_view(self._menu_view)

def main():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    main()