import pandas as pd
import numpy as np

tournament_file = pd.read_csv("ICricketWC2022set.csv")
batter_file = pd.read_csv("WC2022batters.csv")
bowler_file = pd.read_csv("WC2022bowlers.csv")
final_data_sheet = tournament_file[['match_id','ball','batting_team','bowling_team','striker','non_striker','bowler']]
over_length = 6
target_batter_file = "targetWC2022batters.csv"
target_bowler_file = "targetWC2022bowlers.csv"
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

#add above columns to data sheet
final_data_sheet['over_type'] = over_type
final_data_sheet['runs_off_bat'] = runs_off_bat
final_data_sheet['bowler_type'] = bowler_type

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

finalbowlerdata = []
for testbowler in bowler_dict.keys():
	test = final_data_sheet[final_data_sheet["bowler"]==testbowler]
	testtype = bowler_dict[testbowler]
	testteam = test["bowling_team"].to_list()[0]
	testrob = test['runs_off_bat'].to_list()
	bowlingapps = len(test.match_id.unique())
	overs = get_over_count(testrob)
	wickets = testrob.count('W')
	bowling_sr = round(get_ball_count(testrob)/wickets,2) if wickets>0 else '-'
	bowling_avg = round(get_run_count(testrob)/wickets,2) if wickets>0 else '-'
	economy = round(over_length*get_run_count(testrob)/get_ball_count(testrob),2)
	overstring = "'"
	bowler = [testbowler,testtype,testteam,bowlingapps,overs,wickets,bowling_sr,bowling_avg,economy]
	for i in range(len(overtypes)):
		cut = test[test['over_type']==overtypes[i]]
		cutballs = cut["runs_off_bat"].to_list()
		for iterator in range(len(cutballs)):
			if cutballs[iterator] == "Eb":
				cutballs[iterator] = "E"
		sumtaken = 0
		hitstaken = []
		card=[]
		
		overstring = overstring+str(round(get_ball_count(cutballs)/(over_length*bowlingapps)))+"/" if i<len(overtypes)-1 else overstring+str(round(get_ball_count(cutballs)/(over_length*bowlingapps)))
		dots = "-"
		if len(cutballs)>0:
			x = cutballs.count(0)/len(cutballs)
			x = x-spindotpcts[i] if testtype == "Spin" else x-pacedotpcts[i]
			x = x*2
			x = x+spindotpcts[i] if testtype == "Spin" else x+pacedotpcts[i]
			x = x*(108-sumtaken)
			x = round(x,0)
			x = int(x)
			if x<0:
				x=0
			if x>108:
				x=108
			if x>0:
				dots = add_pre_to_six_rep(np.base_repr(int(sumtaken),6)) + " - " + add_pre_to_six_rep(np.base_repr(int(x+sumtaken-1),6))
			else:
				dots = "-"
			sumtaken = sumtaken+x
			hitstaken.append(0)

			def addrating(hittype):
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
						cardval = add_pre_to_six_rep(np.base_repr(int(sumtaken),6)) + " - " + add_pre_to_six_rep(np.base_repr(int(variable+sumtaken-1),6))
					sumtaken = sumtaken+variable
					return cardval if variable>0 else "-"
				else:
					return "-"

			w = addrating("W")
			s = addrating(6)
			f = addrating(4)
			o = addrating(1)
			e = addrating("E")
			t = addrating(2)
			th = addrating(3)
			fi = addrating(5)
			
		else:
			x = o = t = f = s = e = w = th = fi = "-"
			sumtaken = 108
		
		if sumtaken==108:
			#print("GOOD - bowler data generated correctly  ", testbowler)
			card = [dots,w,s,f,o,e,t,th,fi]
			for val in card:
				bowler.append(val)
		else:
			print("BAD  - weird thing happened             ", testbowler)
	bowler.append(overstring)
	finalbowlerdata.append(bowler)
BowlerDF = pd.DataFrame(finalbowlerdata)
BowlerDF.columns = ["name","type","team","bowling_apps","overs","wickets","bowling_sr","bowling_avg","economy","PP0","PPW","PP6","PP4","PP1","PPE","PP2","PP3","PP5","MO0","MOW","MO6","MO4","MO1","MOE","MO2","MO3","MO5","DO0","DOW","DO6","DO4","DO1","DOE","DO2","DO3","DO5","overstr"]
BowlerDF.to_csv(target_bowler_file)


finalbatterdata = []
for testbatter in list(batter_file["striker"].to_list()):
	test = final_data_sheet[final_data_sheet["striker"]==testbatter]
	testteam = test["batting_team"].to_list()[0]
	testrob = test['runs_off_bat'].to_list()
	innings = len(test.match_id.unique())
	ballsfaced = get_ball_count(testrob)
	wickets = testrob.count('W')
	batting_sr = round(100*get_run_count(testrob)/ballsfaced,2) if ballsfaced>0 else '-' 
	batting_avg = round(get_run_count(testrob)/wickets,2) if wickets>0 else '-' #could be innacurate due to runouts
	batter = [testbatter,testteam,innings,ballsfaced,batting_sr,batting_avg]

	#pace
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
	for clist in cardlist:
		for v in clist:
			batter.append(v)
			cc = cc+1
	print(batter)
	finalbatterdata.append(batter)
BatterDF = pd.DataFrame(finalbatterdata)
BatterDF.columns = ["name","team","innings","ballsfaced","batting_sr","batting_avg","PaPP0","PaPPW","PaPP6","PaPP4","PaPP1","PaPPE","PaPP2","PaPP3","PaPP5","PaMO0","PaMOW","PaMO6","PaMO4","PaMO1","PaMOE","PaMO2","PaMO3","PaMO5","PaDO0","PaDOW","PaDO6","PaDO4","PaDO1","PaDOE","PaDO2","PaDO3","PaDO5","SpPP0","SpPPW","SpPP6","SpPP4","SpPP1","SpPPE","SpPP2","SpPP3","SpPP5","SpMO0","SpMOW","SpMO6","SpMO4","SpMO1","SpMOE","SpMO2","SpMO3","SpMO5","SpDO0","SpDOW","SpDO6","SpDO4","SpDO1","SpDOE","SpDO2","SpDO3","SpDO5"]
BatterDF["type"] = batter_file["type"]
BatterDF.to_csv(target_batter_file)