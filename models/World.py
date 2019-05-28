import arcade
from .Rocket import Rocket
from .Cloud import Cloud
from .ComponentList import ComponentList
from .MissileManager import MissileManager
from .MatchStat import MatchStat
from .ScoreFileManager import ScoreFileManager
import time

import sys
sys.path.append('..')
from scenes.MatchStatScene import MatchStatScene

class World():

    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height, gameRestart):

        self.width = width
        self.height = height

        self._state = World.STATE_FROZEN

        self.destroyedMissileAmount = 0
        self.playTime = 0

        self.setup_rocket()
        self.setup_missile_manager(fileName='word/word.txt')
        self.setup_components()
        self.setup_cloud()

        self.config_rocket()
        self.config_component()
        self.config_cloud()

        self.gameReady = False
        self.gameover = False

        self.pressing_key = 0
        self.next_level_time = 10

        self.gameRestart = gameRestart

    def setup_rocket(self):
        scale = 1.3
        self.rocket = Rocket(width=self.width, height=self.height, x=110, y=-120)
        self.rocket.append_texture(arcade.load_texture('images/rocket6.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket5.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket4.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket3.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket2.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket1.png',scale=scale))
        self.rocket.append_texture(arcade.load_texture('images/rocket.png',scale=scale))

    def setup_missile_manager(self, fileName):
        rocket_body_position = self.rocket.right + 90
        self.missile_manager = MissileManager(self.width, self.height, missileTarget=rocket_body_position, wordFileName=fileName, on_missile_destroy=self.on_missile_destroy, on_missile_hit=self.on_missile_hit)

    def setup_components(self):
        self.componentList = ComponentList()
        self.cockpit = arcade.Sprite('images/cockpit.png')

    def setup_cloud(self):
        cloudAmount = 5
        self.cloud_list = arcade.SpriteList()
        self.cloud_list.sprite_list = list(map(lambda x : Cloud(self.width, self.height + 50), range(cloudAmount)))

    def config_rocket(self):
        self.rocket.set_texture(6)
        self.rocket.texture_change_frame = 8

    def config_component(self):
        bottom_of_screen = 50
        self.cockpit.center_x = self.width//2
        self.cockpit.center_y = bottom_of_screen
        self.componentList.add_component(self.cockpit)

    def config_cloud(self):
        self.add_cloud_texture('images/cloud.png')

    def add_component(self, component):
        self.componentList.add_component(component)

    def add_cloud_texture(self, texture):
        for cloud in self.cloud_list:
            cloud.append_texture(arcade.load_texture(texture))
            cloud.set_texture(0)

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def start_game_timer(self):
        self.startTime = time.time()

    def is_started(self):
        return self.state == World.STATE_STARTED

    def draw(self):

        if not self.gameover and not self.rocket.is_destroyed():
            self.cloud_list.draw()
            self.rocket.draw()
            self.missile_manager.draw()
            self.componentList.draw()
            self.draw_stat_bar()
        elif not self.rocket.is_out_of_screen():
            self.rocket.draw()
        elif self.rocket.is_out_of_screen():
            self.matchStatScene.draw()

    def draw_stat_bar(self):
        arcade.draw_text('RocketTyper', 100, 25, arcade.color.BLACK, font_size=25)
        self.draw_health_bar()
        self.draw_missile_count()
        self.draw_time()

    def draw_health_bar(self):
        arcade.draw_rectangle_filled(self.width//2, 35, 305, 55, color=arcade.color.WHITE)
        arcade.draw_rectangle_filled(self.width//2, 35/100 * self.rocket.health, 305, 60 / 100 * self.rocket.health, color=arcade.color.ORANGE_RED)
        arcade.draw_text('HEALTH', self.width//2 - 50, 25, arcade.color.BLACK, font_size=25)

    def draw_missile_count(self):
        arcade.draw_text(str(f'Word: {self.destroyedMissileAmount}'), self.width//2 + 175, 25, arcade.color.BLACK, font_size=22)

    def draw_time(self):
        arcade.draw_text(str(f'Time: {self.playTime:.2f} s'), self.width//2 + 300, 25, arcade.color.BLACK, font_size=22)

    def update(self):

        if self.state == World.STATE_FROZEN:
            return

        self.rocket.update()
        self.rocket.update_animation()

        if not self.gameover:
            if self.ready_to_draw() and not self.rocket.is_destroyed():
                self.componentList.update()
                self.cloud_list.update()
                self.update_play_time()
                self.update_level()
                self.missile_manager.update(self.pressing_key)
            else:
                self.check_game_status()

    def update_level(self):
        level_up_time = 10
        if self.playTime >= level_up_time:
            self.missile_manager.increase_level()
            self.next_level_time += 10

    def update_play_time(self):
        self.playTime = time.time() - self.startTime

    def on_missile_destroy(self):
        self.destroyedMissileAmount += 1

    def on_missile_hit(self):
        self.rocket.hit_by_missile()

    def on_gameover(self):
        self.matchStatScene = MatchStatScene(self.width, self.height, self.destroyedMissileAmount, self.playTime)

    def check_game_status(self):
        if self.rocket.at_ready_position() and not self.gameReady:
            self.gameReady = True
            self.start_game_timer()
        elif self.rocket.is_destroyed() and self.rocket.is_out_of_screen():
            self.on_gameover()
            self.gameover = True

    def is_over(self):
        return self.gameover

    def ready_to_draw(self):
        return self.gameReady

    def on_key_press(self, key):
        self.pressing_key = key