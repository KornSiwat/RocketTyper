import arcade

import sys
sys.path.append('..')
from models.World import World
from models.Rocket import Rocket
from models.Route import Route

class PlayingScene():
	def __init__(self, router):
		self.world = World()

		self.router = router

	def draw(self):
		self.world.draw()

	def update(self):
		self.world.start()
		self.world.update()

	def on_key_press(self, key):
		if self.world.gameover:
			if key == arcade.key.ENTER:
				self.gameRestart()
				self.router.change_route(Route.menu)
		self.world.on_key_press(key)

	def gameRestart(self):
		self.world = World()
