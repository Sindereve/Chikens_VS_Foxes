import arcade
from gameGrid import GameGrid

class GameView(arcade.View):

    def __init__(self, last_view):
        super().__init__()
        self.__last_view = last_view
        self.game_grid = GameGrid()

    def on_draw(self):
        """Отображаем экран игры"""
        arcade.start_render()
        self.game_grid.draw()

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
        """Обновление игры"""
        pass