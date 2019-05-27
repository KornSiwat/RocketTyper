import arcade

class Rocket(arcade.AnimatedTimeSprite):
    def __init__(self, x, y, speed=7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y

        self.health = 100
        self.speed = speed

        self.active = True

    def update(self):
        self.update_animation()

        if not self.at_ready_position():
            self._move_up()

        if self.is_over() and not self.is_out_of_screen():
            self._move_down()

        self.check_health()

    def hit_by_missile(self):
        self.health -= 10

    def at_ready_position(self):
        middle_of_screen = self.height//2
        at_middle_of_screen = self.rocket.center_y >= middle_of_screen
        return middle_of_screen

    def is_out_of_screen(self):
        return self.top < 0

    def is_destroyed(self):
        return not self.active

    def check_health(self):
        if self.health <= 0:
            self.active = False

    def move_up(self):
        self.center_y += self.speed

    def move_down(self):
        self.center_y -= self.speed