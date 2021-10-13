
k = 40

baseRank = 100.0

import csv

class Team(object):
    def __init__(self,name,rank):
        #assert (type(name) == str and type(rank) == float)
        self.name = name
        self.rank = rank


    def __str__(self):
        return self.name


    def __lt__(self,other):
        return self.rank < other.rank

    def getRank(self):
        return self.rank

    def getName(self):
        return self.name
    
    def setRank(self, new_rank):
        self.rank = new_rank
    


def calcExpectation(teamA,teamB):
    '''
    Using Elo Rating System for calculation expectation values

    inupts : teamA, teamB are of Team Class

    output is a expectation of weather A wins over B
    '''

    #assert type(teamA) == Team and type(teamB) == Team

    rankA = teamA.getRank()
    rankB = teamB.getRank()


    expectationA = 1/(1+10**((rankB-rankA)/400))
   

    return expectationA


def updateRanks(result, teamA, teamB):

    '''
    The inputs : results is float 
    teamA and teamB are Team objects

    expected format for results is 
    1 if A wins over B
    0 if B wins over A
    0.5 if the match is a draw
    '''

    #assert type(result) == float and type(teamA) == Team and type(teamB) == Team

    oldRankA = teamA.getRank()
    oldRankB = teamB.getRank()

    expected = calcExpectation(teamA,teamB)

    global k

    new_rankA = oldRankA + k*(result-expected)
    new_rankB = oldRankB + k*(result+expected-1)

    teamA.setRank(new_rankA)
    teamB.setRank(new_rankB)

    return None



class Match(object):

    def __init__(self, teamA, teamB,draw= False):
        '''
        The class assumes the teamA won or drawn over Team B
        '''
        
       # assert type(teamA)== Team and type(teamB) == Team and type(draw) == bool

        self.teamA = teamA
        self.teamB = teamB
        self.draw = draw

    def __str__(self):
        if self.draw:
            return f"Match between"
            
        else : 
            return f"Match between {self.teamA} and {self.teamB}\n{self.teamA} won the game"

    def getWinner(self):
        if self.draw:
            return None
        else:
            return self.teamA
    
    def getResult(self):
        if self.draw:
            return 0.5
        else : 
            return 1

    def getTeams(self):
        return (self.teamA,self.teamB)
        
    


rows = []
with open("./matches.csv",'r') as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

#print(header)
#print(rows)

teamsLookup = {}

allTeams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions', 'Rising Pune Supergiant', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Daredevils', 'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers', 'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants']

for team in allTeams:
    teamsLookup[team] = Team(team,baseRank)

print(len(rows))
matches = []
for row in rows:
    winner = row[10]
    if winner != "":
        if winner != row[4]:
            loser = row[5]
        else :
            loser = row[4]
        matches.append(Match(teamsLookup[winner],teamsLookup[loser]))
    else :
        matches.append(Match(teamsLookup[row[4]],teamsLookup[row[5]],draw=True))



from prettytable import PrettyTable

def Main():

    print(f"No of Matches : {len(matches)}")
    for match in matches:
        teamA,teamB = match.getTeams()
        updateRanks(match.getResult(),teamA,teamB)
    
    teams = []
    for team in teamsLookup.keys():
        teams.append(teamsLookup[team])
    
    teams.sort(reverse=True)

    myTable = PrettyTable(['RANK','TEAM','RATEING'])

    i = 0
    for team in teams:
        i+=1
        myTable.add_row([i,team.name,"{:.2f}".format(team.rank)])
    
    print(myTable)
Main()