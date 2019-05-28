import arcade
from .Route import Route
from .Router import Router
from .MenuChoiceSprite import MenuChoiceSprite
from .World import World
from .Rocket import Rocket
from .Missile import Missile
from .ScoreFileManager import ScoreFileManager
from .FpsCounter import FpsCounter
import time

import sys
sys.path.append('..')

from Config import Config
from scenes.MenuScene import MenuScene
from scenes.PlayingScene import PlayingScene
from scenes.InstructionScene import InstructionScene
from scenes.ScoreBoardScene import ScoreBoardScene

class RocketTyperWindow(arcade.Window):
    def __init__(self):
        super().__init__(width=Config.SCREEN_WIDTH, height=Config.SCREEN_HEIGHT)
        self.width = Config.SCREEN_WIDTH
        self.height = Config.SCREEN_HEIGHT
        self.background = arcade.load_texture("images/background.png")

        self.router_setup()
        self.menu_setup(self.width, self.height)
        self.game_setup(self.width, self.height)
        self.instruction_setup(self.width, self.height)
        self.scoreboard_setup(self.width, self.height)

        self.router_config()

        self.fpsCounter = FpsCounter()
        
        self.set_update_rate(Config.FPS)

    def menu_setup(self, width, height):
        self.menuScene = MenuScene(self.router)

    def game_setup(self, width, height):
        self.playingScene = PlayingScene(self.router)

    def instruction_setup(self, width, height):
        self.instructionScene = InstructionScene(self.router)

    def scoreboard_setup(self, width, height):
        self.scoreboardScene = ScoreBoardScene(self.router) 

    def router_setup(self):
        self.router = Router()

    def router_config(self):
        routes = {Route.menu : self.menuScene,
                Route.game: self.playingScene,
                Route.instruction: self.instructionScene,
                Route.scoreboard: self.scoreboardScene }
        self.router.routes = routes
        self.router.current_scene = self.router.routes[Route.menu]

    def update(self, delta):
        self.router.current_scene.update()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height, self.background)

        self.router.current_scene.draw()
        self.fpsCounter.tick()

    def draw_fps(self):
        arcade.draw_text(f"fps{self.fpscounter.fps():.2f}", 6,self.size_height - 18, arcade.color.BLACK)

    def draw_game(self):
        self.world.draw()

    def on_key_press(self, key, key_modifiers):
        self.router.current_scene.on_key_press(key)
