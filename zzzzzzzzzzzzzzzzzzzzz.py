import arcade

# Константы для окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game Info Table"

class GameInfoView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_SLATE_BLUE

    def on_draw(self):
        arcade.start_render()

        # Рисуем фон таблички
        table_x = SCREEN_WIDTH // 2
        table_y = SCREEN_HEIGHT // 2
        table_width = 400
        table_height = 300

        arcade.draw_rectangle_filled(table_x, table_y, table_width, table_height, arcade.color.LIGHT_GRAY)
        arcade.draw_rectangle_outline(table_x, table_y, table_width, table_height, arcade.color.BLACK, 4)

        # Заголовок таблички
        arcade.draw_text("Game Info", table_x, table_y + table_height // 2 - 40, 
                         arcade.color.BLACK, 24, anchor_x="center", font_name="Arial")

        # Текст описания
        info_text = (
            "Welcome to Chickens vs Fox!\n"
            "Rules:\n"
            "- Control the chickens to protect the farm.\n"
            "- Beware of the foxes!\n"
            "- Use arrow keys to move.\n"
            "- Press ESC to return to menu.\n"
        )
        arcade.draw_text(info_text, table_x - table_width // 2 + 20, table_y + table_height // 2 - 80, 
                         arcade.color.DARK_BLUE, 16, width=table_width - 40, align="left")

        # Кнопка "OK"
        button_width = 100
        button_height = 40
        button_x = table_x
        button_y = table_y - table_height // 2 + 50
        arcade.draw_rectangle_filled(button_x, button_y, button_width, button_height, arcade.color.GREEN)
        arcade.draw_rectangle_outline(button_x, button_y, button_width, button_height, arcade.color.BLACK, 2)
        arcade.draw_text("OK", button_x, button_y - 10, arcade.color.BLACK, 18, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """Закрыть табличку при нажатии на кнопку 'OK'."""
        table_x = SCREEN_WIDTH // 2
        table_y = SCREEN_HEIGHT // 2 - 300 // 2 + 50  # положение кнопки
        button_width = 100
        button_height = 40

        if (table_x - button_width // 2 <= x <= table_x + button_width // 2 and
            table_y - button_height // 2 <= y <= table_y + button_height // 2):
            print("OK clicked!")
            self.window.show_view(None)  # Закрыть табличку, вернуться в игру или меню.

# Основной запуск
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    info_view = GameInfoView()
    window.show_view(info_view)
    arcade.run()

if __name__ == "__main__":
    main()
