import arcade

import sys
sys.path.append('..')
from models.World import World
from models.Rocket import Rocket

class PlayingScene():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.world = World(width=width, height=height, gameRestart=self.gameRestart)

	def draw(self):
		self.world.draw()

	def update(self):
		self.world.start()
		self.world.update()

	def on_key_press(self, key):
		self.world.on_key_press(key)

	def gameRestart(self):
		self.world = World(width=self.width, height=self.height, gameRestart=self.gameRestart)
