import time
from .Slot import Slot
from .WordManager import WordManager
from .ReadWordFile import ReadWordFile
from random import choice

class MissileManager():
    ''' class for the missile manager of the game which is responsible the for the missile deployment, missile destroy '''

    def __init__(self, width, height, missileTargetPosition, wordFileName, on_missile_destroy, on_missile_hit):
        self.missileTargetPosition = missileTargetPosition
        self.attack_zone_x = [missileTargetPosition, width]
        self.attack_zone_y = [150, height]
        self.level = 0
        self.hard_level = 5
        self.updated_level = False
        self.slot_list = []
        missile_height=100
        for y_pos in range(self.attack_zone_y[1],200, -(missile_height)):
            self.slot_list.append(Slot(self.attack_zone_x, y_pos-50, self.missileTargetPosition))
        self.wait_time = 3
        self.deploy_amount = 1
        self.current_slot = None
        self.on_missile_hit = on_missile_hit
        self.on_missile_destroy = on_missile_destroy
        self.timer = time.time()

        self.setup_word_manager(wordFileName)

    def setup_word_manager(self, path):

        self.word_manager = WordManager(ReadWordFile(path).get_list())
        for slot in self.slot_list:
            slot.add_word_manager(self.word_manager)
    
    def draw(self):
        for slot in self.slot_list:
            slot.draw()

    def update(self, key):

        self.check_deploy_time()
        self.update_pos()
        self.key_handle(key)
        # self.update_level()

    def update_pos(self):
        for slot in self.get_used_slot():
            slot.update_pos()

    def key_handle(self,key):
        if self.current_slot == None or self.current_slot.is_selected() == False:
            for slot in self.get_used_slot():
                slot.update_key(key)
                if slot.is_selected() == True:
                    self._current_slot = slot
                    key = 0
                    break
        elif self.current_slot.is_use() == True:
            self.current_slot.update_key(key)

    def check_deploy_time(self):
        ''' check whether it is time to deploy the missile or not based on the wait_time attribute
        if the time since the time in timer attribute is more than the value of wait_tume attribute deploy function will be called
        '''

        if time.time() - self.timer >= self.wait_time:
            self.deploy()
            self.timer = time.time()

    def deploy(self):
        '''
        random a slot from a list of free slot (if there is a free slot) then call the create missile function and pass in the word
        which is from generate function of word_manager attribute
        '''

        for _ in range(self.deploy_amount):
            if self.have_free_slot() == True:
                    choice(self.get_free_slot()).create_missile(self.word_manager.generate())

    def get_free_slot(self):
        return [slot for slot in self.slot_list if not slot.is_use()]

    def get_used_slot(self):
        return [slot for slot in self.slot_list if slot.is_use()]

    def have_free_slot(self):
        ''' return true if there is a free slot and return false if there is none '''

        for slot in self.slot_list:
            if not slot.is_use():
                return True
        return False

    def _update_level(self):
        pass

    def reached_hard_level(self):
        return self.level == self.hard_level

    def _change_difficulty(self,wait_time=2, deploy_amount=2, increase_speed=False):
        if not self.updated_level:
            self.word_manager.set_level(self.level//2)
            self.wait_time = wait_time
            self.deploy_amount = deploy_amount
            if increase_speed:
                self.increase_missile_speed()
            self.updated_level = True

    def increase_missile_speed(self):
        for slot in self.slot_list:
            if slot.get_level() != self.level:
                slot.increase_missile_speed()
                slot.set_level(self.level)

    def increase_level(self):
        ''' increase the value of the level attribute by one if its value is less than ten '''

        if self.level < 15:
            self.level += 1
            self.updated_level = False

