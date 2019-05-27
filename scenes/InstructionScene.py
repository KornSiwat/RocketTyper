import arcade

class InstructionScene():
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._background = arcade.load_texture("images/background.png")
        self._grayBackground = arcade.load_texture("images/result.png")
        self._header = arcade.Sprite()
        self._header.append_texture(arcade.load_texture('images/howtoplay.png'))
        self._header.set_texture(0)
        self._instructionPic = arcade.load_texture('images/instruction.png')

    def draw(self):
        ''' draw instruction route element '''

        arcade.draw_texture_rectangle(self._width//2 , self._height//2 , self._width-250, self._height-150, self._grayBackground)

        self.draw_header()

        arcade.draw_texture_rectangle(self._width//2 , self._height//2 ,self._width-250, self._height-150 ,self._instructionPic)

    def draw_header(self):
        self._header.center_x = self._width//2
        self._header.center_y = self._height//2 + 205
        self._header.draw()