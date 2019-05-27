from .Missile import Missile

class Slot():

    def __init__(self, x, y, target, word_manager):

        self.word_manager = word_manager
        self.being_used = False
        self.selected = False
        self.x_position = x
        self.y_position = y
        self.missile = None
        self.target = target
        self._missile_speed = 1
        self.level = 1

    def create_missile(self, word):
        self.missile = Missile(self.x_position, self.y_position , word=word, target=self.target, speed=self.missile_speed)
        self.in_use = True

    def draw(self):
        if self.missile != None:
            self.issile.draw_with_word()

    def update_pos(self):

        self.missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        self.missile.update_key(key)

    def is_use(self):
        return self.being_used

    def is_selected(self):
        return self._selected

    def check_missile_status(self):
        if self.missile.is_selected() == True:
            self.selected = True
        if self.missile.is_active() == False:
            self.delete_missile()

    def delete_missile(self):
        self.word_manager.recycle(self.missile.get_first_alphabet())
        self.missile = None
        self.in_use = False
        self.selected = False

    def increase_missile_speed(self):
        increasing_amount = 0.5
        self.missile_speed += increasing_amount

    def set_level(self, level):
        self.level = level
