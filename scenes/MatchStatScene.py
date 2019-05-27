import arcade

import sys
sys.path.append('..')
from models.ScoreFileManager import ScoreFileManager
from models.MatchStat import MatchStat

class MatchStatScene():
    def __init__(self, width, height, destoryedMissileAmount, playTime):
        self.width = width
        self.height = height

        self.setup_background()

        self.setup_scoreManager()
        self.setup_matchStat(destoryedMissileAmount, playTime)
        self.config_scoreManager()
        self.config_stat()



    def setup_scoreManager(self):
        self.scoreManager = ScoreFileManager('../score.txt')

    def setup_matchStat(self, destoryedMissileAmount, playTime):
        wordPerMinute = destoryedMissileAmount/(playTime/60)
        self.matchStat = MatchStat(destoryedMissileAmount, wordPerMinute, playTime)

    def setup_background(self):
        self.background = arcade.load_texture('images/result.png')

    def config_scoreManager(self):
        self.scoreManager.write(self.matchStat)
        self.scoreManager.read()

    def draw(self):
        self.draw_background()
        self.draw_stat()

    def draw_text(self, x, y, word='', font_size=30):
        arcade.draw_text(word, self._width//2 + x, self._height//2 + y, color=arcade.color.BLACK, font_size=font_size)

    def draw_background(self):
        arcade.draw_texture_rectangle(self._width//2 , self._height//2 , self._width-250, self._height-150, result)

    def draw_stat(self):
        for text in self.config_stat:
            self.draw_text(x=text[0], y=text[1], word=text[2], font_size=text[3])

    def config_stat(self):
        self.to_draw = [
            [-50, 195, 'Result', 35],
            [-230, 110, f'Total Words: {self.matchStat.destoryedMissileAmount}', 30],
            [-230, 30, f'Total Time: {self.matchStat.totalTime}', 30],
            [-230, -50, f'Speed: {self.matchStat.wordPerMinute} WPM', 30],
            [-230, -130, f'Local Best Time: {self._scoreManager.get_best().totalTime:.2f} s', 30],
            [-260, -210, f'Press Enter To Go Back To Menu', 37],
        ]
