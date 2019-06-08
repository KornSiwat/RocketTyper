from .Missile import Missile


class Slot():
    def __init__(self, x_position, y_position, target, word_manager, on_missile_destroy, on_missile_hit):
        self.x_position = x_position
        self.y_position = y_position

        self.word_manager = word_manager
        self.on_missile_destroy = on_missile_destroy
        self.on_missile_hit = on_missile_hit

        self.config_slot(target)

    def config_slot(self, target):
        self.missile_target = target
        self.missile_speed = 1

        self.missile = None

        self.in_use = False
        self.selected = False

    def create_missile(self, word):
        self.missile = Missile(
            self.x_position, self.y_position, word, self.missile_target, self.missile_speed)
        self.in_use = True

    def draw(self):
        if self.missile != None:
            self.missile.draw_with_word()

    def update_missile_position(self):
        self.missile.update_position()
        self.check_missile_status()

    def update_key(self, key):
        self.missile.update_key(key)

    def is_use(self):
        return self.in_use

    def is_selected(self):
        return self.selected

    def check_missile_status(self):
        if self.missile.is_selected():
            self.selected = True
        if not self.missile.is_active():
            self.delete_missile()

    def delete_missile(self):
        if self.missile.do_damage():
            self.on_missile_hit()
        else:
            self.on_missile_destroy()

        self.word_manager.recycle_alphabet(self.missile.get_first_alphabet())
        self.set_initial_config()

    def set_initial_config(self):
        self.missile = None
        self.in_use = False
        self.selected = False

    def increase_missile_speed(self):
        increasing_amount = 0.5
        self.missile_speed += increasing_amount
