import arcade

class GameView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.message = "Game in Progress!"

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.message, self.window.width // 2, self.window.height // 2,
                         arcade.color.WHITE, 24, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        # Нажмите любую клавишу, чтобы показать результат
        if symbol == arcade.key.ENTER:
            result_view = ResultView(self, self.window)
            self.window.show_view(result_view)


class ResultView(arcade.View):
    def __init__(self, game_view, window):
        super().__init__(window)
        self.game_view = game_view
        self.transparency = 150  # Уровень прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

    def on_draw(self):
        # Сначала рисуем содержимое предыдущего view (GameView)
        self.game_view.on_draw()

        # Добавляем полупрозрачный фон поверх
        arcade.draw_rectangle_filled(self.window.width // 2, self.window.height // 2,
                                     self.window.width, self.window.height,
                                     (0, 0, 0, self.transparency))

        # Отображаем текст результата
        arcade.draw_text("YOU WIN!", self.window.width // 2, self.window.height // 2,
                         arcade.color.YELLOW, 36, anchor_x="center", bold=True)

    def on_key_press(self, symbol, modifiers):
        # Возвращаемся к игровому экрану
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Overlay Example")
        self.current_view = GameView(self)
        self.show_view(self.current_view)


if __name__ == "__main__":
    MyGame()
    arcade.run()
