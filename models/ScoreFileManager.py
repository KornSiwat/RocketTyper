from .MatchStat import MatchStat


class ScoreFileManager():
    def __init__(self, name):
        self.file_name = name
        self.matchStatList = []

    def read(self):
        with open(self.file_name, 'r') as file:
            file = file.readlines()
            score_list = [x.strip().split(',') for x in file if len(x) > 1]
        for line in score_list:
            for i in range(len(line)):
                line[i] = float(line[i])
        self.score_list = score_list
        for line in self.score_list:
            self.matchStatList.append(
                MatchStat(wordAmount=line[0], wordPerMinute=line[1], totalTime=line[2]))

    def write(self, matchStat):
        with open(self.file_name, 'a') as file:
            file.write(
                f'\n{matchStat.wordAmount},{matchStat.wordPerMinute:.2f},{matchStat.totalTime:.2f}')

    def get_best_time(self):
        return sorted(self.score_list, key=lambda x: x[1], reverse=True)[0][2]

    def get_latest_five(self):
        result = self.matchStatList[::-1]
        return result[0:5]
