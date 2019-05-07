from models import WordManager, ReadWordFile

a = WordManager(ReadWordFile('word/word.txt').get_list())
print(a.get_short())
print(a.get_long())