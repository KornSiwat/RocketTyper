import arcade

import sys
sys.path.append('..')
from models.ScoreFileManager import ScoreFileManager
from models.Route import Route
from Config import Config

class ScoreBoardScene():
    def __init__(self, router):
        self.width = Config.SCREEN_WIDTH
        self.height = Config.SCREEN_HEIGHT

        self.setup_score_manager()

        self.setup_assets()
        self.config_header()
        self.setup_table()
        self.config_background()

        self.router = router

    def setup_score_manager(self):
        self.score_manager = ScoreFileManager('score.txt')
        self.score_manager.read()

    def setup_assets(self):
        self.header = arcade.Sprite()

        self.grayBackground = arcade.load_texture("images/result.png")
        self.scoreboardBackground = arcade.load_texture('images/scoreboardbg.png')
        self.header.append_texture(arcade.load_texture('images/scoreboard.png'))

    def config_header(self):
        self.header.center_x = self.width//2
        self.header.center_y = self.height//2 + 205
        self.header.set_texture(0)

    def setup_table(self):
        self.config_table_header()
        self.config_table_body()
        self.config_table_footer()

    def config_background(self):
        self.background_width = self.width-250
        self.background_height = self.height-150

    def config_table_header(self):
        self.table_data = [
            [-280, 100, 'No.'],
            [-200, 100, 'Words'],
            [-75, 100, 'Word Per Minute'],
            [170, 100, 'Total Time']
        ]

    def config_table_body(self):
        for no, matchStat in enumerate(self.score_manager.get_latest_five(),1):
            self.table_data.append([-270, 90-(30 * no), str(no)])
            self.table_data.append([-180, 90-(30 * no), f'{matchStat.wordAmount:02.2f}'])
            self.table_data.append([0, 90-(30 * no), f'{matchStat.wordPerMinute:02.2f}'])
            self.table_data.append([200, 90-(30 * no), f'{matchStat.totalTime:02.2f}'])

    def config_table_footer(self):
        self.table_data.append([-320, -120, f'Local Best Time: {self.score_manager.get_best_time():.2f} s'])
        self.table_data.append([-320, -160, f'World Best Time: Feature Coming Soon'])

    def draw_text(self, x, y, word=''):
        arcade.draw_text(word, self.width//2 + x, self.height//2 + y, color=arcade.color.BLACK, font_size=23)

    def draw_texture(self, width, height, texture):
        arcade.draw_texture_rectangle(self.width//2 , self.height//2, width=width, height=height,texture=texture)

    def draw(self):
        self.draw_background()
        self.draw_header()
        self.draw_table()

    def draw_background(self):
        self.draw_texture(width=self.background_width, height=self.background_height, texture=self.grayBackground)
        self.draw_texture(width=self.background_width, height=self.background_height, texture=self.scoreboardBackground)

    def draw_header(self):
        self.header.draw()

    def draw_table(self):
        for row in self.table_data:
            self.draw_text(row[0], row[1], row[2])

    def update(self):
        pass

    def on_key_press(self, key):
        if key == arcade.key.ESCAPE:
            self.router.change_route(Route.menu)
