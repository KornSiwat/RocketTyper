import arcade
import sys

sys.path.append('..')
from models.Route import Route
from Config import Config

class InstructionScene():
    def __init__(self, router):
        self.width = Config.SCREEN_WIDTH
        self.height = Config.SCREEN_HEIGHT

        self.setup_assets()
        self.setup_header()
        self.setup_background()

        self.router = router

    def setup_assets(self):
        self.background = arcade.load_texture("images/background.png")
        self.gray_background = arcade.load_texture("images/result.png")
        self.header = arcade.Sprite()
        self.header.append_texture(arcade.load_texture('images/howtoplay.png'))
        self.instruction_pic = arcade.load_texture('images/instruction.png')

    def setup_header(self):
        self.header.center_x = self.width//2
        self.header.center_y = self.height//2 + 205
        self.header.set_texture(0)

    def setup_background(self):
        self.background_width = self.width-250
        self.background_height = self.height-150

    def draw(self):
        self.draw_background()
        self.draw_header()

    def draw_texture(self, width, height, texture):
        arcade.draw_texture_rectangle(self.width//2 , self.height//2, width=width, height=height,texture=texture)

    def draw_background(self):
        self.draw_texture(width=self.background_width, height=self.background_height, texture=self.gray_background)
        self.draw_texture(width=self.background_width, height=self.background_height, texture=self.instruction_pic)

    def draw_header(self):
        self.header.draw()

    def update(self):
        pass

    def on_key_press(self, key):
        if key == arcade.key.ESCAPE:
            self.router.change_route(Route.menu)
