import arcade

class ScoreBoardScene():
    def __init__(self, width, height, scoreManager, assetManager=0):
        self._width = width
        self._height = height
        self.assetManager = assetManager
        self._grayBackground = arcade.load_texture("images/result.png")
        self._scoreboardBackground = arcade.load_texture('images/scoreboardbg.png')
        self._scoreManager = scoreManager
        self._scoreboardPic = arcade.load_texture('images/scoreboard.png')
        self._header = arcade.Sprite()
        self._header.append_texture(arcade.load_texture('images/scoreboard.png'))
        self._header.set_texture(0)

    def draw(self):
        ''' draw scoreboard scene element '''

        self.draw_background()
        self.draw_header()
        self.draw_table()
        self.draw_table_info()
        self.draw_high_score()

    def draw_background(self):
        arcade.draw_texture_rectangle(self._width//2 , self._height//2 , self._width-250, self._height-150, self._grayBackground)
        arcade.draw_texture_rectangle(self._width//2 , self._height//2 , self._width-250, self._height-150 , self._scoreboardBackground)

    def draw_header(self):
        self._header.center_x = self._width//2
        self._header.center_y = self._height//2 + 205
        self._header.draw()

    def draw_table(self):
        arcade.draw_text('No.', self._width//2 - 280, self._height//2 + 100, arcade.color.BLACK, font_size=23)
        arcade.draw_text('Words', self._width//2 - 200, self._height//2 + 100, arcade.color.BLACK, font_size=23)
        arcade.draw_text('Word Per Minute', self._width//2 - 75, self._height//2 + 100, arcade.color.BLACK,font_size=23)
        arcade.draw_text('Total Time', self._width//2 + 170, self._height//2 + 100, arcade.color.BLACK, font_size=23)

    def draw_table_info(self):
            for no, score in enumerate(self._scoreManager.get_latest_five(),1):
                arcade.draw_text(f'{no}', self._width//2 - 270, self._height//2 + 90 - 30 * no, arcade.color.BLACK, font_size=23)
                arcade.draw_text(f'{score[0]:02.2f}', self._width//2 - 180, self._height//2 + 90 - 30 * no, arcade.color.BLACK, font_size=23)
                arcade.draw_text(f'{score[2]}', self._width//2 , self._height//2 + 90 - 30 * no, arcade.color.BLACK, font_size=23)
                arcade.draw_text(f'{score[1]}', self._width//2 + 200, self._height//2 + 90 - 30 * no, arcade.color.BLACK, font_size=23)

    def draw_high_score(self):
        arcade.draw_text(f'Local Best Time: {self._scoreManager.get_best()[1]:.2f} s', self._width//2 - 320, self._height//2 - 120, arcade.color.BLACK, font_size=23)
        arcade.draw_text(f'World Best Time: Feature Coming Soon', self._width//2 - 320, self._height//2 - 160, arcade.color.BLACK, font_size=23)