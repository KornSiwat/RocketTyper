import arcade

import sys
sys.path.append('..')
from models.World import World
from models.Rocket import Rocket

class PlayingScene():
	def __init__(self, router):
		self.world = World(gameRestart=self.gameRestart)

		self.router = router

	def draw(self):
		self.world.draw()

	def update(self):
		self.world.start()
		self.world.update()

	def on_key_press(self, key):
		self.world.on_key_press(key)

	def gameRestart(self):
		self.world = World(gameRestart=self.gameRestart)
