import arcade
from random import randint

class Cloud(arcade.Sprite):
    INSTANCE_NUMBER = 0

    def __init__(self, width, height, speed=7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._screen_height = height
        self._screen_width = width
        self._speed = speed
        self.center_x = randint(0, self._screen_width)
        self.center_y = self._screen_height + (self.INSTANCE_NUMBER * 300)

        Cloud.INSTANCE_NUMBER += 1

    def update(self):
        self.center_y -= self._speed
        if self.out_of_screen():
            self._reuse()

    def out_of_screen(self):
        return self.center_y + self.top < 0

    def _reuse(self):
        self.center_x = randint(100, self._screen_width)
        self.center_y = self._screen_height + 300
