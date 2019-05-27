import arcade
from random import randint

class Cloud(arcade.Sprite):
    ''' class for cloud element'''

    INSTANCE_NUMBER = 0

    def __init__(self, width, height, speed=7, *args, **kwargs):
        ''' create attributes of cloud instance '''

        super().__init__(*args, **kwargs)
        self._screen_height = height
        self._screen_width = width
        self._speed = speed
        self.center_x = randint(0, self._screen_width)
        self.center_y = self._screen_height + (self.INSTANCE_NUMBER * 300)

        Cloud.INSTANCE_NUMBER += 1

    def update(self):
        ''' update the position of the cloud instance '''

        self.center_y -= self._speed
        if self.out_of_screen():
            self._reuse()

    def out_of_screen(self):
        ''' check the position of the cloud instance and return True if the cloud is out of the screen '''

        if self.center_y + self.top < 0:
            return True
        return False

    def _reuse(self):
        ''' call when the cloud instance is out of the screen to random the x position of the cloud and release it from the top of the screen '''

        self.center_x = randint(100, self._screen_width)
        self.center_y = self._screen_height + 300