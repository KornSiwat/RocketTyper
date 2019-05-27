import arcade
from .Cloud import Cloud
from .ComponentList import ComponentList
from .MissileManager import MissileManager
from .MatchStat import MatchStat
from .ScoreFileManager import ScoreFileManager
import time

class World():

    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height, gameRestart):

        self.width = width
        self.height = height

        self._state = World.STATE_FROZEN

        self._missile_count = 0
        self._time = 0

        self.componentList = ComponentList()

        self.gameRestart = gameRestart

    def setup_rocket(self, rocket):
        scale = 1.3
        self.rocket = rocket(x=110, y=-120)
        self.rocket.load_texture(arcade.load_texture('images/rocket6.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket5.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket4.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket3.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket2.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket1.png',scale=scale))
        self.rocket.load_texture(arcade.load_texture('images/rocket.png',scale=scale))

    def setup_missileManager(self, fileName):
        rocket_body_position = self.rocket.right-50
        self._missile_manager = MissileManager(self.width, self.height, missileTargetPosition=rocket_body_position, wordFileName=fileName)

    def setup_scoreManager(self):
        self._scoreManager = ScoreFileManager('../score.txt')

    def setup_components(self):
        self.cockpit = arcade.Sprite('images/cockpit.png')
        # self.cockpit.load_texture(arcade.load_texture())

    def setup_cloud(self):
        cloudAmount = 5
        self.cloud_list = arcade.SpriteList()
        self.cloud_list.sprite_list = list(map(lambda x : Cloud(self.width, self.height), range(cloudAmount)))

    def config_rocket(self):
        self.rocket.set_texture(8)
        self.rocket.texture_change_frame = 8

    def config_component(self):
        bottom_of_screen = 50
        self.cockpit.center_x = self.width//2
        self.cockpit.center_y = bottom_of_screen
        # self.cockpit.set_texture(0)
        self.componentList.add_component(self.cockpit)

    def config_cloud(self):
        self.add_cloud_texture('images/cloud.png')

    def add_component(self, component):
        self.componentList.add_component(component)

    def add_cloud_texture(self, texture):
        for cloud in self._cloud_list:
            cloud.load_texture(arcade.load_texture(texture))
            cloud.set_texture(0)

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def start_game_timer(self):
        self._start_time = time.time()

    def is_started(self):
        return self._state == World.STATE_STARTED

    def draw(self):

        self.componentList.draw()
        self.draw_stat()
        self.rocket.draw()
        self._missile_manager.draw()
        self.cloud_list.draw()

    def draw_stat_bar(self):
        arcade.draw_text('RocketTyper', 100, 25, arcade.color.BLACK, font_size=25)
        self._draw_rocket_health()
        self._draw_missile_count()
        self._draw_time()

    def draw_health_bar(self):
        arcade.draw_rectangle_filled(self._width//2, 35, 305, 55, color=arcade.color.WHITE)
        arcade.draw_rectangle_filled(self._width//2, 35/100*self._rocket.get_health(), 305, 60/100*self._rocket.get_health(), color=arcade.color.ORANGE_RED)
        arcade.draw_text('HEALTH', self._width//2 - 50, 25, arcade.color.BLACK, font_size=25)

    def _draw_missile_count(self):
        arcade.draw_text(str(f'Word: {self._missile_count}'), self._width//2 + 175, 25, arcade.color.BLACK, font_size=22)

    def _draw_time(self):
        arcade.draw_text(str(f'Time: {self._time:.2f} s'), self._width//2 + 300, 25, arcade.color.BLACK, font_size=22)

    def update(self):

        if self._state == World.STATE_FROZEN:
            return
        self._rocket.update()
        self._rocket.update_animation()
        self.check_rocket_in_ready_position()
        if self._is_over() == False:
            self._components.update()
            self._cloud_list.update()
            self._update_time()
            self._update_level()
        self._check_gameover()


    def update_level(self):
        if self._time >= self._next_level_time:
            self._missile_manager.increase_level()
            self._next_level_time += 10

    def update_play_time(self):
        self.playTime = time.time() - self._startTime

    def on_missile_destroy(self):
        self.destroyed_missile_counter += self._missile_manager.get_missile_count()

    def on_hit_by_missile(self):
        self.rocket.hitByMissile()

    def gameover(self):
        self.gameover = True

    def is_over(self):
        return self.gameover

    def on_key_press(self, key):
        self._pressing_key = key