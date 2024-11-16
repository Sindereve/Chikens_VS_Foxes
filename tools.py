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

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        """
        Init button 
        :param action: Func for button
        """
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.is_hovered = False

    def on_draw(self):
        """ Draw """
        color = button_color if self.is_hovered else (92, 219, 20)
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        arcade.draw_text(self.text, self.x - self.width / 2 + 10, self.y - self.height / 4, text_color, 18)

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
        


class AnimatedBackground(arcade.Sprite):
    def __init__(self, image_folder, x, y, scale=1):
        super().__init__()
        
        # list frames
        self.frames = []  
        self.frame_index = 0  
        
        # loading frames
        self.load_frames(image_folder)  
        self.set_position(x, y)
        self.scale = scale  

    def load_frames(self, folder):
        """ loading full frame """
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                filepath = os.path.join(folder, filename)
                self.frames.append(arcade.load_texture(filepath))

    def update(self):
        """ update sprite image"""
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0  
        self.texture = self.frames[self.frame_index]  

    def draw(self):
        """ DRAW """
        super().draw()