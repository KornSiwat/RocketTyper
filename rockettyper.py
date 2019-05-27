import arcade
from models.RocketTyperWindow import RocketTyperWindow

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

if __name__ == '__main__':
    window = RocketTyperWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
