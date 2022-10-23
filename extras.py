import pandas as pd
import numpy as np

tournament_file = pd.read_csv("ICricketWC2022set.csv")
bowler_file = pd.read_csv("WC2022bowlers.csv")

droplist = []
for i in range(len(tournament_file['ball'].to_list())):
	if tournament_file['ball'].to_list()[i] == 'ball':
		droplist.append(i)
tournament_file = tournament_file.drop(droplist)
bowler_dict = {} #includes 'bowler name': 'type'
for i in range(len(bowler_file['bowler'].to_list())):
	bowler_dict[bowler_file['bowler'][i]] = bowler_file['type'][i]
bowler_type = []
for x in tournament_file['bowler'].to_list():
	bowler_type.append(bowler_dict[x])
tournament_file['bowler_type'] = bowler_type

#CHANGE SPIN/PACE TYPE
types = ["Spin","Pace"]


for x in types:
    print(x)
    cutfile = tournament_file[tournament_file["bowler_type"]==x]
    nb = cutfile['noballs'].to_list()
    wd = cutfile['wides'].to_list()
    b = cutfile['byes'].to_list()
    lb = cutfile['legbyes'].to_list()


    def getactualextras(lst):
        test = []
        for x in lst:
            try: 
                test.append(int(x))
            except:
                continue
        return test
    noballs = getactualextras(nb)
    wides = getactualextras(wd)
    byes = getactualextras(b)
    legbyes = getactualextras(lb)

    no_of_extras = len(noballs)+len(wides)+len(byes)+len(legbyes)

    possiblenb = list(dict.fromkeys(noballs))
    possiblewd = list(dict.fromkeys(wides))
    possibleb = list(dict.fromkeys(byes))
    possiblelb = list(dict.fromkeys(legbyes))
    def add_pre_to_six_rep(sixrep):
        text = ""
        for i in range(len(sixrep)):
            text=text+str(int(sixrep[i])+1)
        if len(text)==3:
            return text
        if len(text)==2:
            return "1"+text
        if len(text)==1:
            return "11"+text

    cnt = 0
    for x in possiblenb:
        if round(216*noballs.count(x)/no_of_extras)>0:
            val = add_pre_to_six_rep(np.base_repr(cnt,6)) + "-" + add_pre_to_six_rep(np.base_repr(cnt+round(216*noballs.count(x)/no_of_extras)-1,6))
            cnt = cnt + round(216*noballs.count(x)/no_of_extras)
            print(str(x)+"nb", val)
    for x in possiblewd:
        if round(216*wides.count(x)/no_of_extras)>0:
            val = add_pre_to_six_rep(np.base_repr(cnt,6)) + "-" + add_pre_to_six_rep(np.base_repr(cnt+round(216*wides.count(x)/no_of_extras)-1,6))
            cnt = cnt + round(216*wides.count(x)/no_of_extras)
            print(str(x)+"wd", val)
    for x in possibleb:
        if round(216*byes.count(x)/no_of_extras)>0:
            val = add_pre_to_six_rep(np.base_repr(cnt,6)) + "-" + add_pre_to_six_rep(np.base_repr(cnt+round(216*byes.count(x)/no_of_extras)-1,6))
            cnt = cnt + round(216*byes.count(x)/no_of_extras)
            print(str(x)+"b", val)
    for x in possiblelb:
        if round(216*legbyes.count(x)/no_of_extras)>0: 
            val = add_pre_to_six_rep(np.base_repr(cnt,6)) + "-" + add_pre_to_six_rep(np.base_repr(cnt+round(216*legbyes.count(x)/no_of_extras)-1,6))
            cnt = cnt + round(216*legbyes.count(x)/no_of_extras)
            print(str(x)+"lb", val)

