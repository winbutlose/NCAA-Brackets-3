import json, random

def getTempo(team,teamdata):
    print(team)
    print(teamdata[team[1].lower()]["adjt"])
    return teamdata[team[1].lower()]["adjt"]

def getADJOff(team,teamdata):
    print("adjo for "+str(team[1]))
    print(teamdata[team[1].lower()]["adjo"])
    return teamdata[team[1].lower()]["adjo"]

def getADJDef(team,teamdata):
    print("adjd for "+str(team[1]))
    print(teamdata[team[1].lower()]["adjd"])
    return teamdata[team[1].lower()]["adjd"]


def DetermineWinner(a,b,teamdata):
    print()
    print(a[1] + " vs " + b[1])
    tempo = (getTempo(a,teamdata) * getTempo(b,teamdata)) / 67.6
    print("tempo = "+ str(tempo))
    aScore = (getADJOff(a,teamdata) * getADJDef(b,teamdata)) / 100; #a offense * b defense / league avg
    bScore = (getADJOff(b,teamdata) * getADJDef(a,teamdata)) / 100; #a offense * b defense / league avg
    print("ascore="+str(aScore))
    print("bscore="+str(bScore))
    aPoints = (aScore * tempo) / 100
    bPoints = (bScore * tempo) / 100

    #Bonus Multipliers
    #Some things to ensure games don't get too wild
    if int(a[0]) < int(b[0]):
        aPoints += aPoints * .35
    elif int(b[0]) < int(a[0]):
            bPoints += bPoints * .35
    elif int(a[0]) == int(b[0]):
        pass

    if int(a[0]) < 5:
        aPoints += aPoints * .3
    if int(b[0]) < 5:
        bPoints += bPoints * .3

    print("INITIAL==" + a[1] + "'s points: " + str(aPoints) + " - " + b[1] + "'s points: " + str(bPoints))

    totalPoints = aPoints + bPoints
    print("AFTER==" + a[1] + "'s points: " + str(aPoints) + " - " + b[1] + "'s points: " + str(bPoints) + " Total Points = " + str(totalPoints))
    #pick winner randomly
    #double winner = (Math.random() * totalPoints);
    winner = random.uniform(0.0,1.0)*totalPoints
    print("random # = " + str(winner))
    if (winner < aPoints):
        print("WINNER = **" + a[1] + "**")
        return a

    print("WINNER = **" + b[1] + "**")
    return b


def SimRound(data,teamdata,numgames):
    winners = [['0', 'Placeholder']]
    for game in range (1,numgames):
        winners.append(DetermineWinner(data[game],data[(numgames*2-1)-game],teamdata))
    print(winners)
    return(winners)

f = open('flask/static/tourneyInfo.json')
data = json.load(f)
ff = open('flask/static/teams.json')
teamdata = json.load(ff)

west = data["seeds"]["west"]
east = data["seeds"]["east"]
midwest = data["seeds"]["midwest"]
south = data["seeds"]["south"]

R2W = SimRound(west,teamdata,9)
R2E = SimRound(east,teamdata,9)
R2MW = SimRound(midwest,teamdata,9)
R2S = SimRound(south,teamdata,9)

print(R2W)

S16W = SimRound(R2W,teamdata,5)
S16E = SimRound(R2E,teamdata,5)
S16MW = SimRound(R2MW,teamdata,5)
S16S = SimRound(R2S,teamdata,5)

E8W = SimRound(S16W,teamdata,3)
E8E = SimRound(S16E,teamdata,3)
E8MW = SimRound(S16MW,teamdata,3)
E8S = SimRound(S16S,teamdata,3)

E8 = [['0', 'Placeholder']]
E8.append(E8W[1])
E8.append(E8E[1])
E8.append(E8MW[1])
E8.append(E8S[1])
E8.append(E8S[2])
E8.append(E8MW[2])
E8.append(E8E[2])
E8.append(E8W[2])

print(E8)

FF = SimRound(E8,teamdata,5)

Chip = SimRound(FF,teamdata,3)

Champion = DetermineWinner(Chip[1],Chip[2],teamdata)
print(Champion)

f.close()
ff.close()