from .Missile import Missile

class Slot():
    ''' class for slots in the missile manager which each instance has its own y position and responsible for missile in the x range of position '''

    def __init__(self, x, y, target, level=1):
        ''' create attributes for slot instance '''

        self._word_manager = None
        self._in_use = False
        self._selected = False
        self._x_points = x
        self._y_pos = y
        self._missile = None
        self._wait_pixel = 0
        self._target = target
        self._damage = 0
        self._missile_count = 0
        self._missile_speed = 1
        self._level = level

    def add_word_manager(self, word_managaer):
        ''' assign the word_manager parameter to word_manager attribute '''

        self._word_manager = word_managaer

    def create_missile(self, word):
        ''' create the missile which the position, the target coordinate, and the speed based on attributes of instance
        and the word from word parameter then reassign the value of the in_use attribute with True to indicate that the slot instance
        has a missile in it.
        '''

        self._missile = Missile(self._x_points[1], self._y_pos, word=word, target=self._target, speed=self._missile_speed)
        self._in_use = True

    def draw(self):
        ''' call a draw function of the missile instance if there is a missile instance binding to missile attribute '''

        if self._missile != None:
            self._missile.draw_with_word()

    def update_pos(self):
        ''' call functions to update position and check the status of the missile instance binding to missile attribute '''

        self._missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        ''' call update_key and pass in the key parameter to the missile instance binding to missile attribute
        in order to check whether the key pressed matched with char of the missile.
        '''

        self._missile.update_key(key)

    def is_use(self):
        ''' return whether the instance is currently having a missile or not '''
        return self._in_use

    def is_selected(self):
        ''' return whether the missile of instance has been matched with the key pressed or not '''

        return self._selected

    def check_missile_status(self):
        ''' check the value from the missile instance an update the value of attributes
        if the missile has been selected the selected instace will be reassign to True
        and if the missile status is not active the delete_missile function will be called
        '''

        if self._missile.is_selected() == True:
            self._selected = True
        if self._missile.is_active() == False:
            self._delete_missile()

    def _delete_missile(self):
        ''' 
        Add a value from missile get_damage method to the damage attribute
        If the damage from get_damage method is zero, it means that the missile is set to inactive by typing in the word completely 
        so missile_count attribute will be added by one.
        Then the first of alphabet of the word attached to the missile will be pass to recycle method of the word manager attribute
        to make the word starts with recycled alphabet able to be generated again.
        Lastly, reassign the value of missile releted attribute to be as there is no missile.
        '''
        self._damage += self._missile.get_damage()
        if self._missile.get_damage() == 0:
            self._missile_count += 1
        self._word_manager.recycle(self._missile.get_first_alphabet())
        self._missile = None
        self._in_use = False
        self._selected = False

    def _increase_missile_speed(self):
        ''' Increase the missile_speed attribute by half which make the missile that will be created move faster '''
        self._missile_speed += 0.5

    def set_level(self, level):
        ''' Assign a value from level parameter to the level attribute '''

        self._level = level

    def get_level(self):
        ''' return an int value of the level attribute '''

        return self._level

    def get_damage(self):
        ''' return an int value of the damage attribute '''

        return self._damage

    def reset_damage(self):
        ''' reset the value of the damage attribute by reassigining its value to zero. '''

        self._damage = 0

    def get_missile_count(self):
        ''' return an int value of the missile_count attribute '''

        return self._missile_count

    def reset_missile_count(self):
        ''' reset the value of the missile_count attribute by reassigining its value to zero. '''

        self._missile_count = 0


