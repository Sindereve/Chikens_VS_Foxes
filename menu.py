import arcade

# Константы для кнопки
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = arcade.color.LIGHT_BLUE
HOVER_COLOR = arcade.color.DARK_BLUE
TEXT_COLOR = arcade.color.WHITE
FONT_SIZE = 20
SHADOW_COLOR = arcade.color.GRAY
SHADOW_OFFSET = 5  # Смещение тени

class ButtonWithShadow:
    def __init__(self, x, y, width, height, text, on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click
        self.is_hovered = False

    def draw(self):
        """Рисует кнопку с тенью и контуром"""
        # Рисуем тень
        if self.is_hovered:
            shadow_color = arcade.color.DARK_GRAY
        else:
            shadow_color = SHADOW_COLOR

        arcade.draw_lrtb_rectangle_filled(self.x - self.width // 2 + SHADOW_OFFSET, 
                                          self.x + self.width // 2 + SHADOW_OFFSET, 
                                          self.y + self.height // 2 + SHADOW_OFFSET, 
                                          self.y - self.height // 2 + SHADOW_OFFSET, 
                                          shadow_color)

        # Рисуем кнопку с основным цветом
        if self.is_hovered:
            color_start = arcade.color.DARK_BLUE
            color_end = arcade.color.BLUE
        else:
            color_start = arcade.color.LIGHT_BLUE
            color_end = arcade.color.BLUE

        arcade.draw_lrtb_rectangle_filled(self.x - self.width // 2, 
                                          self.x + self.width // 2, 
                                          self.y + self.height // 2, 
                                          self.y - self.height // 2, 
                                          color_start)
        
        # Рисуем контур для 3D эффекта
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.BLACK, 3)

        # Рисуем текст на кнопке
        arcade.draw_text(self.text, self.x - self.width // 2, self.y - self.height // 4,
                         TEXT_COLOR, FONT_SIZE, width=self.width, align="center")

    def check_for_click(self, x, y):
        """Проверяет, был ли клик по кнопке"""
        if (self.x - self.width // 2 < x < self.x + self.width // 2 and
            self.y - self.height // 2 < y < self.y + self.height // 2):
            return True
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        """Проверяет, наводит ли курсор на кнопку"""
        self.is_hovered = (self.x - self.width // 2 < x < self.x + self.width // 2 and
                           self.y - self.height // 2 < y < self.y + self.height // 2)