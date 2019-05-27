from .MatchStat import MatchStat

class ScoreFileManager():
    ''' class for ScoreFileRw which is responsible for reading and writing the score file '''

    def __init__(self,name):
        ''' create attributes of and ScoreFileRW instance '''

        self.file_name = name
        self.matchStatList = []

    def read(self):
        ''' open the file from the path stored in file_name attribute and read and split them by the colon and convert the data type from
        string to float and store them as a nested list which each lists contains the stats of the match played
        '''

        with open( self.file_name , 'r') as file:
            file = file.readlines()
            score_list = [x.strip().split(',') for x in file if len(x) > 1]
        for line in score_list:
            for i in range(len(line)):
                line[i] = float(line[i])
        self.score_list = score_list
        for line in self.score_list:
            self.matchStatList.append(MatchStat(wordAmount=line[0], wordPerMinute=line[1], totalTime=line[2]))

    def write(self, matchStat):
        '''open the file from the path stored in file_name attribute and append the string containing the stats from score_lst parameter to the last line of the text file '''

        with open( self.file_name, 'a') as file:
            file.write(f'\n{matchStat.wordAmount},{matchStat.wordPerMinute:.2f},{matchStat.totalTime:.2f}')

    def get_best(self):
        ''' return the list containing the stats of the match that has the longest play time '''

        return sorted(self.score_list,key=lambda x: x[1], reverse=True)[0]

    def get_latest_five(self):
        ''' return the list containg the stats list of lastest five match '''

        result = self.matchStatList[::-1]
        return result[0:5]

