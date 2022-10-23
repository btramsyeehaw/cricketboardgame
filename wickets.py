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
#CHANGE SPIN/PACE TYPE
types = ["Spin","Pace"]
for x in types:
    print(x)
    cutfile = tournament_file[tournament_file["bowler_type"]==x]
    w = cutfile['wicket_type'].to_list()
    wkts = []
    cnt = 0
    for x in w:
        if str(x)!='nan' and str(x)!='wicket_type':
            wkts.append(x)
            cnt = cnt+1
    possiblewkts = list(dict.fromkeys(wkts))
    possiblewkts.sort()
    c = 0
    for wk in possiblewkts:
        if round(216*wkts.count(wk)/cnt)>0:
            val = add_pre_to_six_rep(np.base_repr(c,6)) + "-" + add_pre_to_six_rep(np.base_repr(c+round(216*wkts.count(wk)/cnt)-1,6))
            c = c + round(216*wkts.count(wk)/cnt)
            print(wk, val)