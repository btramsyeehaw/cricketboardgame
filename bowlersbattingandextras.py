import pandas as pd
import numpy as np

tournament_file = pd.read_csv("2022TheHundred.csv")
batter_file = pd.read_csv("2022HundoBatters.csv")
bowler_file = pd.read_csv("2022HundoBowlers.csv")
final_data_sheet = tournament_file[['match_id','ball','batting_team','bowling_team','striker','non_striker','bowler']]
over_length = 6
target_batter_file = "targetHundoBatters.csv"
target_bowler_file = "targetHundoBowlers.csv"
#remove unwanted rows from main data base
droplist = []
for i in range(len(final_data_sheet['ball'].to_list())):
	if final_data_sheet['ball'].to_list()[i] == 'ball':
		droplist.append(i)
final_data_sheet = final_data_sheet.drop(droplist)
tournament_file = tournament_file.drop(droplist)

bowler_dict = {} #includes 'bowler name': 'type'
for i in range(len(bowler_file['bowler'].to_list())):
	bowler_dict[bowler_file['bowler'][i]] = bowler_file['type'][i]

batter_dict = {} #includes 'bowler name': 'type'
for i in range(len(batter_file['striker'].to_list())):
	batter_dict[batter_file['striker'][i]] = batter_file['type'][i]
#create over type column
over_type = []
for x in final_data_sheet['ball'].to_list():
	if x!='ball':
		if float(x)<6:
			over_type.append("1PP")
		elif float(x)<16:
			over_type.append("2MO")
		else:
			over_type.append("3DO")

#create runs off bat column
runs_off_bat = []
rob = tournament_file['runs_off_bat'].to_list()
ex = tournament_file['extras'].to_list()
wt = tournament_file['wicket_type'].to_list()
nb = tournament_file['noballs'].to_list()
wd = tournament_file['wides'].to_list()
print(nb,wd)
for x in range(len(rob)):
	if rob[x]!='runs_off_bat':
		if str(wt[x])!='nan':
			robgood = 'W'
		elif float(ex[x])>0:
			if float(nb[x])>0.0 or float(wd[x])>0.0:
				robgood = 'Eb'
			else:
				robgood = 'E'
		else:
			robgood = int(rob[x])
		runs_off_bat.append(robgood)

#add bowler type column
bowler_type = []
for x in final_data_sheet['bowler'].to_list():
	bowler_type.append(bowler_dict[x])
batter_type = []
for x in final_data_sheet['striker'].to_list():
    batter_type.append(batter_dict[x])


#add above columns to data sheet
final_data_sheet['over_type'] = over_type
final_data_sheet['runs_off_bat'] = runs_off_bat
final_data_sheet['bowler_type'] = bowler_type
final_data_sheet['batter_type'] = batter_type

#league wide sums
available_values = [0,1,2,3,4,5,6,'E','W']
overtypes = ["1PP", "2MO", "3DO"]
spincounts = [] #sums in 7s: first 7 is powerplay etc
pacecounts = []
spindotpcts = [] 
pacedotpcts = []
for ot in overtypes:
	cut = final_data_sheet[final_data_sheet['over_type']==ot]
	spin = cut[cut["bowler_type"]=="Spin"]
	pace = cut[cut["bowler_type"]=="Pace"]
	for val in available_values:
		spincounts.append(spin["runs_off_bat"].to_list().count(val))
		pacecounts.append(pace["runs_off_bat"].to_list().count(val))
		if val == 0:
			spindotpcts.append(spin["runs_off_bat"].to_list().count(val)/len(spin["runs_off_bat"].to_list()))
			pacedotpcts.append(pace["runs_off_bat"].to_list().count(val)/len(pace["runs_off_bat"].to_list()))			

#create bowler database
def get_over_count(balllist):
	cnt = 0
	for x in balllist:
		if x!='Eb':
			cnt = cnt+1
	return str(cnt//over_length)+"."+str(cnt%over_length)
def get_ball_count(balllist):
	cnt = 0
	for x in balllist:
		if x!='Eb':
			cnt = cnt+1
	return cnt
def get_run_count(balllist):
	cnt = 0
	for x in balllist:
		if x!='Eb' and x!='E' and x!='W':
			cnt = cnt+x
	return cnt

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

test = final_data_sheet[(final_data_sheet["batter_type"]=="Bowler") | (final_data_sheet["batter_type"]=="Bowler OS")]
testrob = test['runs_off_bat'].to_list()
innings = len(test.match_id.unique())
ballsfaced = get_ball_count(testrob)
wickets = testrob.count('W')
batting_sr = round(100*get_run_count(testrob)/ballsfaced,2) if ballsfaced>0 else '-' 
batting_avg = round(get_run_count(testrob)/wickets,2) if wickets>0 else '-' #could be innacurate due to runouts

print([innings,ballsfaced,batting_sr,batting_avg])
testpace = test[test["bowler_type"]=="Pace"]
cardlist = []
for i in range(len(overtypes)):
    cut = testpace[testpace['over_type']==overtypes[i]]
    cutballs = cut["runs_off_bat"].to_list()
    for iterator in range(len(cutballs)):
        if cutballs[iterator] == "Eb":
            cutballs[iterator] = "E"
    sumtaken = 0
    hitstaken = []
    card = []
    dots = "-"
    if len(cutballs)>0:
        x = cutballs.count(0)/len(cutballs)
        x = x-pacedotpcts[i]
        x = x*2
        x = x+pacedotpcts[i]
        x = x*(108-sumtaken)
        x = round(x,0)
        x = int(x)
        if x<0:
            x=0
        if x>108:
            x=108
        if x>0:
            dots = add_pre_to_six_rep(np.base_repr(int(108+sumtaken),6)) + " - " + add_pre_to_six_rep(np.base_repr(int(x+sumtaken+107),6))
        else:
            dots = "-"
        sumtaken = sumtaken+x
        hitstaken.append(0)

        def addbatterrating(hittype):
            global sumtaken
            sumt = 0
            for x in hitstaken:
                sumt = sumt+cutballs.count(x)
            hitstaken.append(hittype)
            if len(cutballs)-sumt>0:
                variable = cutballs.count(hittype)/(len(cutballs)-sumt)
                variable = variable*(108-sumtaken)
                variable = round(variable,0)
                if variable>0:
                    cardval = add_pre_to_six_rep(np.base_repr(108+int(sumtaken),6)) + " - " + add_pre_to_six_rep(np.base_repr(int(variable+sumtaken+107),6))
                sumtaken = sumtaken+variable
                return cardval if variable>0 else "-"
            else:
                return "-"

        w = addbatterrating("W")
        s = addbatterrating(6)
        f = addbatterrating(4)
        o = addbatterrating(1)
        e = addbatterrating("E")
        t = addbatterrating(2)
        th = addbatterrating(3)
        fi = addbatterrating(5)
        
    else:
        x = o = t = f = s = e = w = th = fi = "-"
        sumtaken = 108
    
    if sumtaken==108:
        #print("GOOD - batter data generated correctly  ", testbatter)
        card = [dots,w,s,f,o,e,t,th,fi]
        cardlist.append(card)
    else:
        print("BAD  - weird thing happened             ", testbatter)	
#spin
testspin = test[test["bowler_type"]=="Spin"]
for i in range(len(overtypes)):
    cut = testspin[testspin['over_type']==overtypes[i]]
    cutballs = cut["runs_off_bat"].to_list()
    for iterator in range(len(cutballs)):
        if cutballs[iterator] == "Eb":
            cutballs[iterator] = "E"
    sumtaken = 0
    hitstaken = []
    card = []
    dots = "-"
    if len(cutballs)>0:
        x = cutballs.count(0)/len(cutballs)
        x = x-spindotpcts[i]
        x = x*2
        x = x+spindotpcts[i]
        x = x*(108-sumtaken)
        x = round(x,0)
        x = int(x)
        if x<0:
            x=0
        if x>108:
            x=108
        if x>0:
            dots = add_pre_to_six_rep(np.base_repr(108+int(sumtaken),6)) + " - " + add_pre_to_six_rep(np.base_repr(108+int(x+sumtaken-1),6))
        else:
            dots = "-"
        sumtaken = sumtaken+x
        hitstaken.append(0)

        #addratingdef?
        w = addbatterrating("W")
        s = addbatterrating(6)
        f = addbatterrating(4)
        o = addbatterrating(1)
        e = addbatterrating("E")
        t = addbatterrating(2)
        th = addbatterrating(3)
        fi = addbatterrating(5)
        
    else:
        x = o = t = f = s = e = w = th = fi = "-"
        sumtaken = 108
    
    if sumtaken==108:
        #print("GOOD - batter data generated correctly  ", testbatter)
        card = [dots,w,s,f,o,e,t,th,fi]
        cardlist.append(card)
    else:
        print("BAD  - weird thing happened             ", testbatter)	
empty = ["-","-","-","-","-","-","-","-","-"]
if cardlist[0]==empty and cardlist[3]!=empty:
    cardlist[0]=cardlist[3]
if cardlist[3]==empty and cardlist[0]!=empty:
    cardlist[3]=cardlist[0]
if cardlist[1]==empty and cardlist[4]!=empty:
    cardlist[1]=cardlist[4]
if cardlist[4]==empty and cardlist[1]!=empty:
    cardlist[4]=cardlist[1]
if cardlist[2]==empty and cardlist[5]!=empty:
    cardlist[2]=cardlist[5]
if cardlist[5]==empty and cardlist[2]!=empty:
    cardlist[5]=cardlist[2]

if cardlist[0]==empty:
    if cardlist[1]!=empty:
        cardlist[0]=cardlist[1]
    else:
        cardlist[0]=cardlist[2]
if cardlist[1]==empty:
    if cardlist[2]!=empty:
        cardlist[1]=cardlist[2]
    else:
        cardlist[1]=cardlist[0]
if cardlist[2]==empty:
    if cardlist[1]!=empty:
        cardlist[2]=cardlist[1]
    else:
        cardlist[2]=cardlist[0]
if cardlist[3]==empty:
    if cardlist[4]!=empty:
        cardlist[3]=cardlist[4]
    else:
        cardlist[3]=cardlist[5]
if cardlist[4]==empty:
    if cardlist[5]!=empty:
        cardlist[4]=cardlist[5]
    else:
        cardlist[4]=cardlist[3]
if cardlist[5]==empty:
    if cardlist[4]!=empty:
        cardlist[5]=cardlist[4]
    else:
        cardlist[5]=cardlist[3]
cc = 0
clist = []
for c in cardlist:
    for x in c:
        clist.append(x)
print(clist)