import arcade

import sys
sys.path.append('..')
from models.ScoreFileManager import ScoreFileManager
from models.MatchStat import MatchStat
from Config import Config

class MatchStatScene():
    def __init__(self, destoryedMissileAmount, playTime):
        self.width = Config.SCREEN_WIDTH
        self.height = Config.SCREEN_HEIGHT

        self.setup_background()

        self.setup_score_manager()
        self.setup_match_stat(destoryedMissileAmount, playTime)
        self.config_score_manager()
        self.config_stat()

    def setup_score_manager(self):
        self.score_manager = ScoreFileManager('score.txt')

    def setup_match_stat(self, destoryedMissileAmount, playTime):
        wordPerMinute = destoryedMissileAmount/(playTime/60)
        self.match_stat = MatchStat(destoryedMissileAmount, wordPerMinute, playTime)

    def setup_background(self):
        self.background = arcade.load_texture('images/result.png')

    def config_score_manager(self):
        self.score_manager.write(self.match_stat)
        self.score_manager.read()

    def draw(self):
        self.draw_background()
        self.draw_stat()

    def draw_text(self, x, y, word='', font_size=30):
        arcade.draw_text(word, self.width//2 + x, self.height//2 + y, color=arcade.color.BLACK, font_size=font_size)

    def draw_background(self):
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 , self.width-250, self.height-150, self.background)

    def draw_stat(self):
        for text in self.statList:
            self.draw_text(x=text[0], y=text[1], word=text[2], font_size=text[3])

    def config_stat(self):
        self.statList = [
            [-50, 195, 'Result', 35],
            [-230, 110, f'Total Words: {self.match_stat.wordAmount}', 30],
            [-230, 30, f'Total Time: {self.match_stat.totalTime:.2f} s', 30],
            [-230, -50, f'Speed: {self.match_stat.wordPerMinute:.2f} WPM', 30],
            [-230, -130, f'Local Best Time: {self.score_manager.get_best_time():.2f} s', 30],
            [-260, -210, f'Press Enter To Go Back To Menu', 30],
        ]
