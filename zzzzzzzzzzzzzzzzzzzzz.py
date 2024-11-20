import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Victory Animation"

class VictoryAnimation(arcade.View):
    def __init__(self):
        super().__init__()
        self.confetti = []
        self.text_opacity = 0
        self.text_scale = 1.0
        self.music = None

    def setup(self):
        # Конфетти
        for _ in range(100):
            confetto = {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200),
                "dx": random.uniform(-2, 2),
                "dy": random.uniform(-1, -4),
                "color": random.choice([arcade.color.RED, arcade.color.YELLOW, arcade.color.GREEN,
                                        arcade.color.BLUE, arcade.color.PINK, arcade.color.PURPLE])
            }
            self.confetti.append(confetto)

    def on_draw(self):
        """Отображение победной анимации."""
        arcade.start_render()

        # Фон
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)

        # Конфетти
        for confetto in self.confetti:
            arcade.draw_circle_filled(confetto["x"], confetto["y"], 5, confetto["color"])

        # Текст победы
        arcade.draw_text("YOU WIN!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, 50 * self.text_scale, anchor_x="center", anchor_y="center",
                           width=SCREEN_WIDTH//2, align="center", font_name="fibberish")

    def on_update(self, delta_time):
        """Обновление состояния анимации."""
        # Анимация конфетти
        for confetto in self.confetti:
            confetto["x"] += confetto["dx"]
            confetto["y"] += confetto["dy"]
            if confetto["y"] < 0:
                confetto["x"] = random.randint(0, SCREEN_WIDTH)
                confetto["y"] = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)

        # Анимация текста
        if self.text_opacity < 255:
            self.text_opacity += 5
        if self.text_scale < 2.0:
            self.text_scale += 0.01

    def on_key_press(self, key, modifiers):
        """Нажатие клавиши для выхода."""
        if key == arcade.key.ESCAPE:
            arcade.exit()

def main():
    """Основной метод."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    victory_view = VictoryAnimation()
    victory_view.setup()
    window.show_view(victory_view)
    arcade.run()

if __name__ == "__main__":
    main()
