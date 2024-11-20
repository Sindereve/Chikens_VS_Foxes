import arcade 
import configparser
import os

def load_config(config_file="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def hex_in_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))  

config = load_config()

background_color = (int(config["color scheme"]["background_color_r"]), 
                    int(config["color scheme"]["background_color_g"]),
                    int(config["color scheme"]["background_color_b"]))  
text_color = (int(config["color scheme"]["text_color_r"]),
              int(config["color scheme"]["text_color_g"]),
              int(config["color scheme"]["text_color_b"])) 
button_color = (int(config["color scheme"]["button_color_r"]),
                int(config["color scheme"]["button_color_g"]),
                int(config["color scheme"]["button_color_b"]))

font_path = "assets/fonts/Pixels.ttf"
arcade.load_font(font_path)

class Button:
    def __init__(self,x, y, width, height, text, image_base, image_hover, action=None):
        """
        Init button 
        :param action: Func for button
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._text = text
        self.action = action
        self._normal_texture = arcade.load_texture(image_base)
        self._hover_texture = arcade.load_texture(image_hover)
        self.is_hovered = False

    def draw(self):
        """ Draw """
        current_texture = self._hover_texture if self.is_hovered else self._normal_texture

        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, current_texture)
        arcade.draw_text(self._text,
                    self.x, self.y,
                    arcade.color.WHITE, 30, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        # outline
        #arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.RED, 5)

    def check_click(self, x, y):
        """ is click ??? """
        if (self.x - self.width / 2 <= x <= self.x + self.width / 2 and
            self.y - self.height / 2 <= y <= self.y + self.height / 2):
            if self.action:
                self.action()

    def check_hover(self, x, y):
        """ this is magick for mouse :)))))"""
        self.is_hovered = (self.x - self.width / 2 <= x <= self.x + self.width / 2 and
                           self.y - self.height / 2 <= y <= self.y + self.height / 2)
        self.draw()

class InfoBoard:
    def __init__(self, x, y, width, height, number_chickens, number_foxes, number_step, who_step):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._number_chickens = number_chickens
        self._number_foxes = number_foxes
        self._who_step = who_step
        self._number_step = number_step


    def update_info(self, number_chickens, number_foxes, number_step, who_step):
        self._number_chickens = number_chickens
        self._who_step = who_step
        self._number_foxes = number_foxes
        self._number_step = number_step
        self.draw()

    def draw(self):
        # arcade.draw_texture_rectangle(self._x, self._y, self._width, self._height, self._texture)
        arcade.draw_rectangle_filled(self._x, self._y, self._width, self._height, (211, 211, 211, 200))

        arcade.draw_text('Information',
                    self._x, int(self._y + self._height//2 - 20),
                    arcade.color.BLACK, 30, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        left_edge_text = int(self._x - self._width // 2)
        up_edge_text = int(self._y + self._height//2 - 70)

        arcade.draw_text(f' Step ',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 25, font_name="fibberish")
        up_edge_text-=20
        arcade.draw_text(f'  {self._who_step}',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 25, font_name="fibberish")
        up_edge_text-=20
        arcade.draw_text(f' Number - {self._number_step}',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 25, font_name="fibberish")
        up_edge_text-=50

        arcade.draw_text(f' Count Chicken:',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 20, font_name="fibberish")
        up_edge_text-=20
        arcade.draw_text(f' X {self._number_chickens}',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 25, font_name="fibberish")
        up_edge_text-=50

        
        arcade.draw_text(f' Count Foxes:',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 20, font_name="fibberish")
        up_edge_text-=20
        arcade.draw_text(f' X {self._number_foxes}',
                    left_edge_text , up_edge_text,
                    arcade.color.BLACK, 25, font_name="fibberish")
        up_edge_text-=50

        # outline
        arcade.draw_rectangle_outline(self._x, self._y, self._width, self._height, arcade.color.BLACK, 3)
        
        #draw_rectangle_with_top_left_corner_rounded(self._x, self._y, self._width, self._height, (211, 211, 211, 200), 20)

class ButtonBoard:
    def __init__(self, x, y, width, height, functional = []):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._buttons = self._create_button(functional)

    def _create_button(self, functional):
        buttons = []

        step_in_down = 80
        y_center = int(self._y + self._height*0.3)
        button_width = self._width - 20
        button_height = 70
        


        buttons.append(Button(self._x, y_center, 
                              button_width, button_height, 'Restart',
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-2.png', 
                               ))

        buttons.append(Button(self._x, y_center - step_in_down*len(buttons), 
                              button_width, button_height, 'info',
                              'assets/menuView/button/center_button/folder-1.png', 
                              'assets/menuView/button/center_button/folder-2.png', 
                               ))

        buttons.append(Button(self._x, y_center - step_in_down*len(buttons), 
                              button_width, button_height, 'Exit',
                              'assets/menuView/button/exit_button/folder-2.png', 
                              'assets/menuView/button/exit_button/folder-4.png',
                              functional[0] 
                               ))

        return buttons

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self._buttons:
            button.check_hover(x,y)

    def check_click(self, x, y):
        for button in self._buttons:
            button.check_click(x, y)

    def draw(self):
        """ Draw """

        # arcade.draw_texture_rectangle(self._x, self._y, self._width, self._height, self._texture)
        arcade.draw_rectangle_filled(self._x, self._y, self._width, self._height, (211, 211, 211, 200))

        arcade.draw_text('Menu',
                    self._x, int(self._y + self._height//2 - 20),
                    arcade.color.BLACK, 30, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        for button in self._buttons:
            button.draw()

        arcade.draw_rectangle_outline(self._x, self._y, self._width, self._height, arcade.color.BLACK, 3)

class AnimatedBackground(arcade.Sprite):

    def __init__(self, image_folder, x, y, window_width, window_height, scale=1):
        super().__init__()
        
        # list frames
        self.frames = []  
        self.frame_index = 0  
        
        # loading frames
        self.load_frames(image_folder)  
        self.set_position(x, y)
        self.scale = scale  
        # size window
        self.window_width = window_width 
        self.window_height = window_height

    def load_frames(self, folder):
        """ loading full frame """
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                filepath = os.path.join(folder, filename)
                self.frames.append(arcade.load_texture(filepath))
        self.texture = self.frames[self.frame_index]


    def update(self):
        """ update sprite image"""
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0  
        self.texture = self.frames[self.frame_index]  

    def draw(self):
        """ DRAW """
        width = self.window_width * self.scale
        height = self.window_height * self.scale

        arcade.draw_texture_rectangle(
            self.window_width // 2,
            self.window_height // 2,
            width, height, self.texture)

class BlinkingText:
    def __init__(self, text, x, y, font_size):
        
        self._x = x
        self._y = y
        self._text = text
        self._font_size = font_size

        # alpha - animation effect
        self._alpha = 255
        self._alpha_direction = -1

    def draw(self):
        #arcade.draw_rectangle_filled(self._x, self._y, 300, 50, arcade.color.BLACK, alpha=150)

        arcade.draw_text(self._text, self._x + 3, self._y - 3, 
                    arcade.color.BLACK, self._font_size, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')

        
        arcade.draw_text(self._text, self._x, self._y, (255, 0, 0, self._alpha), 
                    self._font_size, font_name="fibberish", 
                    anchor_x='center', anchor_y='center')
                    #border_width=3, border_color=arcade.color.WHITE)

    def update(self, delta_time):
        self._alpha += self._alpha_direction
        if self._alpha <= 0:
            self._alpha_direction *= -1
            self._alpha = 0 
        elif self._alpha >= 255:
            self._alpha_direction *= -1
            self._alpha = 255