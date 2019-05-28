import string
from random import choice
from .ReadWordFile import ReadWordFile

class WordManager():

    def __init__(self, wordFileName , level=1):

        self.level = level

        self.setup_alphabet()
        self.setup_word_file(wordFileName)
        self.setup_word_list()

    def setup_alphabet(self):
        self.used_alphabet = []
        self.unused_alphabet = list(string.ascii_lowercase)

    def setup_word_file(self, wordFileName):
        self.word_dict = ReadWordFile(wordFileName).get_categorized_list()

    def setup_word_list(self):
        self.short_word = dict()
        self.long_word = dict()

        long_word_length = 5
        for alphabet in self.word_dict:
            self.short_word[alphabet] = []
            self.long_word[alphabet] = []
            for word in self.word_dict[alphabet]:
                if len(word) < long_word_length:
                    self.short_word[alphabet].append(word)
                else:
                    self.long_word[alphabet].append(word)

    def generate(self):
        random_alphabet = self.generate_alphabet()
        random_word = choice(self.short_word[random_alphabet] + self.long_word[random_alphabet] * self.level)
        return random_word

    def generate_alphabet(self):
        random_alphabet = choice(self.unused_alphabet)
        self.used_alphabet.append(random_alphabet)
        self.unused_alphabet.remove(random_alphabet)
        return random_alphabet

    def incerease_long_word(self):
        self.level += 1

    def recycle_alphabet(self, alphabet):
        self.unused_alphabet.append(alphabet)
        self.used_alphabet.remove(alphabet)

