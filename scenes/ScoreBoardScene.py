import arcade

class ScoreBoardScene():
    def __init__(self, width, height, scoreManager):
        self._width = width
        self._height = height

        self._scoreManager = scoreManager

        self.setup_assets()
        self.setup_table()

    def setup_assets(self):
        self._grayBackground = arcade.load_texture("images/result.png")
        self._scoreboardBackground = arcade.load_texture('images/scoreboardbg.png')
        self._background_width = self._width-250
        self._background_height = self._height-150
        self._header = arcade.Sprite()
        self._header.append_texture(arcade.load_texture('images/scoreboard.png'))
        self._header.set_texture(0)

    def draw(self):
        ''' draw scoreboard scene elements '''

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
        for row in self._table_data:
            self.draw_text(row[0], row[1], row[2])

    def setup_table(self):
        self.config_table_header()
        self.config_table_body()

    def config_table_header(self):
        self._table_data = [
            [-280, 100, 'No.'],
            [-200, 100, 'Words'],
            [-75, 100, 'Word Per Minute'],
            [170, 100, 'Total Time']
        ]

    def config_table_body(self):
        for no, matchStat in enumerate(self._scoreManager.get_latest_five(),1):
            self._table_data.append([-270, 90-(30 * no), str(no)])
            self._table_data.append([-180, 90-(30 * no), f'{matchStat.wordAmount:02.2f}'])
            self._table_data.append([0, 90-(30 * no), f'{matchStat.wordPerMinute}'])
            self._table_data.append([200, 90-(30 * no), f'{matchStat.totalTime}'])

    def draw_high_score(self):
        self.draw_text(x=-320, y=-120, word=f'Local Best Time: {self._scoreManager.get_best()[1]:.2f} s')
        self.draw_text(x=-320, y=-160, word=f'World Best Time: Feature Coming Soon')

    def draw_text(self, x, y, word=''):
        arcade.draw_text(word, self._width//2 + x, self._height//2 + y, color=arcade.color.BLACK, font_size=23)

    def draw_texture(self, width, height, texture):
        arcade.draw_texture_rectangle(self._width//2 , self._height//2, width=width, height=height,texture=texture)
