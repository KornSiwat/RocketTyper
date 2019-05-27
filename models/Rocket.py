import arcade

class Rocket(arcade.AnimatedTimeSprite):
    ''' class for Rocket Sprite '''

    def __init__(self, x, y, speed=7, *args, **kwargs):
        ''' create attributes of rocket instance '''

        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self._health = 100
        self._ready = False
        self._speed = speed
        self._active = True

    def update(self):
        ''' update the texture of the rocket and check the position and move it based on the current status '''

        self.update_animation()
        if self._ready == False:
            self._move_up()
        if self.is_over() == True and self._out_of_screen() == False:
            self._move_down()
        self._check_dead()

    def update_health(self, damage):
        ''' subtract the current health of the rocket with the damage parameter '''

        self._health -= damage

    def get_health(self):
        ''' return the current health of the rocket '''

        if self._active == True:
            return self._health
        else:
            return 0

    def is_over(self):
        ''' return the status of the rocket '''

        if self._active == False:
            return True
        else:
            return False

    def ready(self):
        ''' call when the rocket is at its ready position '''

        self._ready = True

    def _out_of_screen(self):
        ''' check the position of the rocket and returns true if it is in the screen else returns false '''

        if self.top > 0:
            return False
        return True

    def _check_dead(self):
        ''' check and update the active status of the rocket based on its health '''

        if self._health <= 0:
            self._active = False

    def _move_up(self):
        ''' move the rocket in upward direction '''

        self.center_y += self._speed

    def _move_down(self):
        ''' move the rocket in downward direction '''

        self.center_y -= self._speed