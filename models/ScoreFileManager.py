class ScoreFileManager():
    ''' class for ScoreFileRw which is responsible for reading and writing the score file '''

    def __init__(self,name):
        ''' create attributes of and ScoreFileRW instance '''

        self.file_name = name
        self.score_list = []

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

    def write(self, score_lst):
        '''open the file from the path stored in file_name attribute and append the string containing the stats from score_lst parameter to the last line of the text file '''

        with open( self.file_name, 'a') as file:
            file.write(f'\n{score_lst[0]},{score_lst[1]:.2f},{score_lst[2]:.2f}')

    def get_score(self):
        ''' return the list from score_list attribute '''

        return self.score_list

    def get_best(self):
        ''' return the list containing the stats of the match that has the longest play time '''

        return sorted(self.score_list,key=lambda x: x[1], reverse=True)[0]

    def get_latest_five(self):
        ''' return the list containg the stats list of lastest five match '''

        result = self.score_list[::-1]
        return result[0:5]

