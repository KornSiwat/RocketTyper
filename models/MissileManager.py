import time
from .Slot import Slot
from .WordManager import WordManager
from .ReadWordFile import ReadWordFile
from random import choice


class MissileManager():
    def __init__(self, width, height, missileTarget, wordFileName, on_missile_destroy, on_missile_hit):
        self.width = width
        self.height = height

        self.missileTarget = missileTarget

        self.on_missile_hit = on_missile_hit
        self.on_missile_destroy = on_missile_destroy

        self.setup_word_manager(wordFileName)
        self.setup_slot()
        self.setup_manager_asset()

        self.config_deployment()

    def setup_word_manager(self, wordFileName):
        self.word_manager = WordManager(wordFileName)

    def setup_slot(self):
        self.slot_list = []
        missile_height = 100
        slot_height = 200
        missile_start_x = self.width
        for y_position in range(self.height, slot_height, -(missile_height)):
            missile_start_y = y_position - 50
            self.slot_list.append(Slot(missile_start_x, missile_start_y, self.missileTarget,
                                       self.word_manager, self.on_missile_destroy, self.on_missile_hit))

    def setup_manager_asset(self):
        self.current_slot = None

    def config_deployment(self):
        self.level = 0
        self.hard_level = 5
        self.wait_time = 3
        self.deploy_amount = 2
        self.deploy_timer = time.time()

    def draw(self):
        for slot in self.slot_list:
            slot.draw()

    def update(self, key):
        self.check_deploy_time()
        self.update_missile_position()
        self.pressing_key_handle(key)

    def update_missile_position(self):
        for slot in self.get_used_slot():
            slot.update_missile_position()

    def pressing_key_handle(self, key):
        no_typing_missile = self.current_slot == None
        if no_typing_missile or not self.current_slot.is_selected():
            for slot in self.get_used_slot():
                slot.update_key(key)
                if slot.is_selected() == True:
                    self.current_slot = slot
                    key = 0
                    break
        elif self.current_slot.is_use() == True:
            self.current_slot.update_key(key)
            key = 0

    def check_deploy_time(self):
        passed_time = time.time() - self.deploy_timer
        if passed_time >= self.wait_time:
            self.deploy()
            self.deploy_timer = time.time()

    def deploy(self):
        if self.have_free_slot():
            random_word = self.word_manager.generate()
            random_slot = self.random_slot()
            random_slot.create_missile(word=random_word)

    def random_slot(self):
        random_slot = choice(self.get_unused_slot())
        return random_slot

    def get_unused_slot(self):
        return [slot for slot in self.slot_list if not slot.is_use()]

    def get_used_slot(self):
        return [slot for slot in self.slot_list if slot.is_use()]

    def have_free_slot(self):
        for slot in self.slot_list:
            if not slot.is_use():
                return True
        return False

    def increase_missile_speed(self):
        for slot in self.slot_list:
                slot.increase_missile_speed()
