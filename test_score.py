from models import ScoreFileRW

a = ScoreFileRW('score.txt')
a.read()
print(len(a.score_list))
print(a.get_best())