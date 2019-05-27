import time
from .Slot import Slot
from .WordManager import WordManager
from .ReadWordFile import ReadWordFile
from random import choice

class MissileManager():
    ''' class for the missile manager of the game which is responsible the for the missile deployment, missile destroy '''

    def __init__(self, width, height, missileTargetPosition, wordFileName, level=0, missile_height=100, hard_level=6):
        self.missileTargetPosition = missileTargetPosition
        self._attack_zone_x = [missileTargetPosition, width]
        self._attack_zone_y = [150, height]
        self._level = level
        self._hard_level = hard_level
        self._updated_level = False
        self._slot_list = []
        for y_pos in range(self._attack_zone_y[1],200, -(missile_height)):
            self._slot_list.append(Slot(self._attack_zone_x, y_pos-50, self.missileTargetPosition))
        self._wait_time = 3
        self._deploy_amount = 1
        self._current_slot = None
        self._damage = 0
        self._missile_count = 0
        self._timer = time.time()

    def setup_manager(self, path):
        ''' use the path parameter to create the word manager instance then assign it to the word_manager attribute of the instance '''

        self._word_manager = WordManager(ReadWordFile(path).get_list())
        for slot in self._slot_list:
            slot.add_word_manager(self._word_manager)
    
    def draw(self):
        for slot in self._slot_list:
            slot.draw()

    def update(self, key):

        self._check_deploy_time()
        self._update_pos()
        self._key_handle(key)
        self._update_damage()
        self._update_missile_count()
        self._update_level()

    def _update_pos(self):
        for slot in self._get_used_slot():
            slot.update_pos()

    def _key_handle(self,key):
        if self._current_slot == None or self._current_slot.is_selected() == False:
            for slot in self._get_used_slot():
                slot.update_key(key)
                if slot.is_selected() == True:
                    self._current_slot = slot
                    key = 0
                    break
        elif self._current_slot.is_use() == True:
            self._current_slot.update_key(key)

    def _update_damage(self):
        ''' get the damage value from each slots to update to damage attribute of the instance then reset damage of each slots to zero '''

        for slot in self._slot_list:
            self._damage += slot.get_damage()
            slot.reset_damage()

    def _update_missile_count(self):
        ''' get the destroyed missile amount from each slots to update the missile count attribute of the instance,
        then reset the missile count amount of each slots to zero.
        '''

        for slot in self._slot_list:
            self._missile_count += slot.get_missile_count()
            slot.reset_missile_count()

    def _check_deploy_time(self):
        ''' check whether it is time to deploy the missile or not based on the wait_time attribute
        if the time since the time in timer attribute is more than the value of wait_tume attribute deploy function will be called
        '''

        if time.time() - self._timer >= self._wait_time:
            self._deploy()
            self._timer = time.time()

    def _deploy(self):
        '''
        random a slot from a list of free slot (if there is a free slot) then call the create missile function and pass in the word
        which is from generate function of word_manager attribute
        '''

        for _ in range(self._deploy_amount):
            if self.have_free_slot() == True:
                    choice(self._get_free_slot()).create_missile(self._word_manager.generate())

    def _get_free_slot(self):
        '''
        return a list of free slots which can be indicated by their is_use() method that return false
        '''

        return [slot for slot in self._slot_list if slot.is_use() == False]

    def _get_used_slot(self):
        '''
        return a list of used slots which can be indicated by their is_use() method that return true
        '''

        return [slot for slot in self._slot_list if slot.is_use() == True]

    def have_free_slot(self):
        ''' return true if there is a free slot and return false if there is none '''

        for slot in self._slot_list:
            if slot.is_use() == False:
                return True
        return False

    def get_damage(self):
        ''' return the int value of the damage attribute of the instance '''

        return self._damage

    def reset_damage(self):
        ''' reset the value of the damage attribute by assigning the value to zero '''

        self._damage = 0 

    def get_missile_count(self):
        ''' return the int value of the missile_count attribute of the instance '''

        return self._missile_count
    
    def reset_missile_count(self):
        ''' reset the value of the missile_count attribute by assigning the value to zero '''

        self._missile_count = 0

    def _update_level(self):
        ''' update the value of attributes based on the level attribute.
        The game will be more difficult as the level attribute incrases.
        '''

        if not self._reach_hard_level() and not self._level_is_odd():
            self._change_difficulty(deploy_amount=2)
        elif self._reach_hard_level() and self._level_is_odd():
            self._change_difficulty(deploy_amount=4, increase_speed=True)

    def _reach_hard_level(self):
        return self._level == self._hard_level

    def _level_is_odd(self):
        return self._level % 2 == 1

    def _change_difficulty(self,wait_time=2, deploy_amount=2, increase_speed=False):
        if self._updated_level == False:
            self._word_manager.set_level(self._level//2)
            self._wait_time = wait_time
            self._deploy_amount = deploy_amount
            if increase_speed:
                self.increase_missile_speed()
            self._updated_level = True

    def increase_missile_speed(self):
        for slot in self._slot_list:
            if slot.get_level() != self._level:
                slot._increase_missile_speed()
                slot.set_level(self._level)

    def increase_level(self):
        ''' increase the value of the level attribute by one if its value is less than ten '''

        if self._level < 15:
            self._level += 1
            self._updated_level = False

