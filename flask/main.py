from flask import Flask, render_template
import json, random

app = Flask(__name__)

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


def DetermineWinner(a,b,teamdata,round):
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
        aPoints += aPoints * .4
    elif int(b[0]) < int(a[0]):
            bPoints += bPoints * .4
    elif int(a[0]) == int(b[0]):
        pass

    if int(a[0]) < 5:
        aPoints += aPoints * .4
    if int(b[0]) < 5:
        bPoints += bPoints * .4

    if round > 2:
        if int(a[0]) < 9:
            aPoints += aPoints * .22
        if int(b[0]) < 9:
            bPoints += bPoints * .22

    if round > 2 and round < 4:
        if int(a[0]) == 6 or int(a[0]) == 8 or int(a[0]) == 11:
            aPoints += aPoints * .1
        if int(b[0]) == 6 or int(b[0]) == 8 or int(b[0]) == 11:
            bPoints += bPoints * .1

    #top seeds exceed in late rounds 
    if round > 3:
        if (int(a[0]) < 5):
            aPoints += aPoints * .3
        if (int(b[0]) < 5):
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


def SimRound(data,teamdata,numgames,round):
    winners = [['0', 'Placeholder']]
    for game in range (1,numgames):
        winners.append(DetermineWinner(data[game],data[(numgames*2-1)-game],teamdata,round))
    print(winners)
    return(winners)



@app.route("/")
def home_page():

    f = open('static/tourneyInfo.json')
    data = json.load(f)
    ff = open('static/teams.json')
    teamdata = json.load(ff)

    west = data["seeds"]["west"]
    east = data["seeds"]["east"]
    midwest = data["seeds"]["midwest"]
    south = data["seeds"]["south"]

    R2W = SimRound(west,teamdata,9,1)
    R2E = SimRound(east,teamdata,9,1)
    R2MW = SimRound(midwest,teamdata,9,1)
    R2S = SimRound(south,teamdata,9,1)

    print(R2W)

    S16W = SimRound(R2W,teamdata,5,2)
    S16E = SimRound(R2E,teamdata,5,2)
    S16MW = SimRound(R2MW,teamdata,5,2)
    S16S = SimRound(R2S,teamdata,5,2)

    E8W = SimRound(S16W,teamdata,3,3)
    E8E = SimRound(S16E,teamdata,3,3)
    E8MW = SimRound(S16MW,teamdata,3,3)
    E8S = SimRound(S16S,teamdata,3,3)

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

    FF = SimRound(E8,teamdata,5,4)

    Chip = [['0', 'Placeholder']]
    Chip.append(DetermineWinner(FF[1],FF[2],teamdata,5))
    Chip.append(DetermineWinner(FF[3],FF[4],teamdata,5))
    print(Chip)


    Champion = DetermineWinner(Chip[1],Chip[2],teamdata,6)
    print(Champion)

    f.close()
    ff.close()
    return render_template("index.html",tourneyInfo=data,R2W=R2W,R2E=R2E,R2MW=R2MW,R2S=R2S,S16W=S16W,S16E=S16E,S16MW=S16MW,S16S=S16S,E8=E8,FF=FF,Chip=Chip,Champion=Champion)

app.run(debug=True)

#["Rk","Team","Seed","Conf","W-L","AdjEM","AdjO","AdjD","AdjT","Luck","AdjEM","OppO","OppD","AdjEM",null,null,null,null,null,null,null,null]