import arcade
import sys

sys.path.append('..')
from models.Route import Route

class InstructionScene():
    def __init__(self, width, height, router):
        self._width = width
        self._height = height

        self.setup_assets()
        self.setup_header()
        self.setup_background()

        self.router = router

    def setup_assets(self):
        self._background = arcade.load_texture("images/background.png")
        self._grayBackground = arcade.load_texture("images/result.png")
        self._header = arcade.Sprite()
        self._header.append_texture(arcade.load_texture('images/howtoplay.png'))
        self._instructionPic = arcade.load_texture('images/instruction.png')

    def setup_header(self):
        self._header.center_x = self._width//2
        self._header.center_y = self._height//2 + 205
        self._header.set_texture(0)

    def setup_background(self):
        self._background_width = self._width-250
        self._background_height = self._height-150

    def draw(self):
        ''' draw instruction route element '''

        self.draw_background()
        self.draw_header()

    def draw_texture(self, width, height, texture):
        arcade.draw_texture_rectangle(self._width//2 , self._height//2, width=width, height=height,texture=texture)

    def draw_background(self):
        self.draw_texture(width=self._background_width, height=self._background_height, texture=self._grayBackground)
        self.draw_texture(width=self._background_width, height=self._background_height, texture=self._instructionPic)

    def draw_header(self):
        self._header.draw()

    def update(self):
        pass

    def on_key_press(self, key):
        if key == arcade.key.ESCAPE:
            self.router.change_route(Route.menu)
