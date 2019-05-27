import arcade
from .MenuChoiceSprite import MenuChoiceSprite
from .World import World
from .Rocket import Rocket
from .Missile import Missile
from .ScoreFileManager import ScoreFileManager
from .FpsCounter import FpsCounter
import time

import sys
sys.path.append('..')

from scenes.MenuScene import MenuScene
from scenes.PlayingScene import PlayingScene
from scenes.InstructionScene import InstructionScene
from scenes.ScoreBoardScene import ScoreBoardScene

choices = {
    0: 'menu',
    1: 'game',
    2: 'instruction',
    3: 'scoreboard'
}

class RocketTyperWindow(arcade.Window):
    ''' Class for game window '''

    def __init__(self, width, height):
        ''' create important attribute for the game '''

        super().__init__(width, height)
        self._window_width = width
        self._window_height = height

        self.background = arcade.load_texture("images/background.png")

        self.menu_setup(width, height)
        self.game_setup(width,height)
        self.instruction_setup(width,height)
        self.scoreboard_setup(width, height)

        self.route_config()

        self.fpsCounter = FpsCounter()
        self.set_update_rate(1/60)

    def menu_setup(self, width, height):
        self.menuScene = MenuScene(width, height, self.on_select_route)

    def game_setup(self, width, height):
        self.playingScene = PlayingScene(width, height)

    def instruction_setup(self, width, height):
        self.instructionScene = InstructionScene(width, height, self.on_select_route)

    def scoreboard_setup(self, width, height):
        self.scoreboardScene = ScoreBoardScene(width, height, self.on_select_route) 

    def route_config(self):
        self._routes = { 'menu': self.menuScene,
                        'game': self.playingScene,
                        'instruction': self.instructionScene,
                        'scoreboard': self.scoreboardScene }
        self.current_route = self._routes['menu']
        self.selecting_choice = 0

    def update(self, delta):
        self.current_route.update()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height,self.background)

        self.current_route.draw()
        self.fpsCounter.tick()

    def draw_fps(self):
        arcade.draw_text(f"fps{self.fpscounter.fps():.2f}", 6,self.size_height - 18,arcade.color.BLACK)

    def draw_game(self):
        self.world.draw()

    def on_key_press(self, key, key_modifiers):
        self.current_route.on_key_press(key)

    def on_select_route(self, route):
        self.current_route = self._routes[route]
