import arcade

class ScoreBoardScene():
    def __init__(self, width, height, scoreManager, assetManager=0):
        self._width = width
        self._height = height

        self.assetManager = assetManager

        self._grayBackground = arcade.load_texture("images/result.png")
        self._scoreboardBackground = arcade.load_texture('images/scoreboardbg.png')
        self._background_width = self._width-250
        self._background_height = self._height-150


        self._scoreManager = scoreManager

        self._scoreboardPic = arcade.load_texture('images/scoreboard.png')

        self._header = arcade.Sprite()
        self._header.append_texture(arcade.load_texture('images/scoreboard.png'))
        self._header.set_texture(0)

        self._header_text = []

    def draw(self):
        ''' draw scoreboard scene element '''

        self.draw_background()
        self.draw_header()
        self.draw_table()
        self.draw_high_score()

    def draw_background(self):
        self.draw_texture(width=self._background_width, height=self._background_height, texture=self._grayBackground)
        self.draw_texture(width=self._background_width, height=self._background_height, texture=self._scoreboardBackground)

    def draw_header(self):
        self._header.center_x = self._width//2
        self._header.center_y = self._height//2 + 205
        self._header.draw()

    def draw_table(self):
        self.draw_table_header()
        self.draw_table_body()

    def draw_table_header(self):
        self.draw_text(x=-280, y=100, word='No.')
        self.draw_text(x=-200, y=100, word='Words')
        self.draw_text(x=-75, y=100, word='Word Per Minute')
        self.draw_text(x=170, y=100, word='Total Time')

    def draw_table_body(self):
        for no, matchStat in enumerate(self._scoreManager.get_latest_five(),1):
            self.draw_text(x=-270, y= 90-(30 * no), word=str(no))
            self.draw_text(x=-180, y= 90-(30 * no), word=f'{matchStat.wordAmount:02.2f}')
            self.draw_text(x=0, y= 90-(30 * no), word=f'{matchStat.wordPerMinute}')
            self.draw_text(x=200, y= 90-(30 * no), word=f'{matchStat.totalTime}')

    def draw_high_score(self):
        self.draw_text(x=-320, y=-120, word=f'Local Best Time: {self._scoreManager.get_best()[1]:.2f} s')
        self.draw_text(x=-320, y=-160, word=f'World Best Time: Feature Coming Soon')

    def draw_text(self, x, y, word=''):
        arcade.draw_text(word, self._width//2 + x, self._height//2 + y, color=arcade.color.BLACK, font_size=23)

    def draw_texture(self, width, height, texture):
        arcade.draw_texture_rectangle(self._width//2 , self._height//2, width=width, height=height,texture=texture)
