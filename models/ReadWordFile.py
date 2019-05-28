class ReadWordFile():

    def __init__(self, file_name=''):

        with open(file_name, 'r') as Fin:
            self.raw_word = [x.strip() for x in Fin.readlines()]
        self.categorized_word = {}
        for word in self.raw_word:
            if word[0].lower() not in self.categorized_word:
                self.categorized_word[word[0].lower()] = [word]
            else:
                self.categorized_word[word[0].lower()].append(word)

    def get_categorized_list(self):
        return self.categorized_word