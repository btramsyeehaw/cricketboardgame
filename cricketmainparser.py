import pandas as pd
import numpy as np
tournament_file = pd.read_csv("2022TheHundred.csv")
bowler_file = pd.read_csv("2022HundoBowlers.csv")
batter_file = pd.read_csv("2022HundoBatters.csv")
final_data_sheet = tournament_file[['ball','batting_team','bowling_team','striker','non_striker','bowler']]
over_type = []
runs_off_bat = []

droplist = []
for i in range(len(final_data_sheet['ball'].to_list())):
	if final_data_sheet['ball'].to_list()[i] == 'ball':
		droplist.append(i)

final_data_sheet = final_data_sheet.drop(droplist)
tournament_file = tournament_file.drop(droplist)
bowler_dict = {}

for i in range(len(bowler_file['bowler'].to_list())):
	bowler_dict[bowler_file['bowler'][i]] = bowler_file['type'][i]


for x in final_data_sheet['ball'].to_list():
	if x!='ball':
		if float(x)<5:
			over_type.append("1PP")
		elif float(x)<16:
			over_type.append("2MO")
		else:
			over_type.append("3DO")


rob = tournament_file['runs_off_bat'].to_list()
ex = tournament_file['extras'].to_list()
wt = tournament_file['wicket_type'].to_list()

for x in range(len(rob)):
	if rob[x]!='runs_off_bat':
		if str(wt[x])!='nan':
			robgood = 'W'
		elif float(ex[x])>0:
			robgood = 'E'
		else:
			robgood = int(rob[x])
		runs_off_bat.append(robgood)
final_data_sheet['over_type'] = over_type
final_data_sheet['runs_off_bat'] = runs_off_bat

bowler_type = []
for x in final_data_sheet['bowler'].to_list():
	bowler_type.append(bowler_dict[x])
final_data_sheet['bowler_type'] = bowler_type


available_values = [0,1,2,3,4,5,6,'E','W']
#league wide sums
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

finalbowlerdata = []

for testbowler in bowler_dict.keys():
	bowler = [testbowler]
	test = final_data_sheet[final_data_sheet["bowler"]==testbowler]
	testtype = bowler_dict[testbowler]
	for i in range(len(overtypes)):
		cut = test[test['over_type']==overtypes[i]]
		cutballs = cut["runs_off_bat"].to_list()
		sumtaken = 0
		hitstaken = []
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
					sumtaken = sumtaken+variable
					return int(variable)
				else:
					return 0

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
			bowler.append([x,o,t,th,f,fi,s,e,w])
		else:
			print("BAD  - weird thing happened             ", testbowler)
	finalbowlerdata.append(bowler)
finaldataframe = pd.DataFrame(finalbowlerdata)
finaldataframe["team"] = bowler_file["team"]
finaldataframe["type"] = bowler_file["type"]



batterlist = batter_file["striker"].to_list()
finalbatterdata = []
for testbatter in batterlist:
	batter = [testbatter]
	test = final_data_sheet[final_data_sheet["striker"]==testbatter]
	testpace = test[test["bowler_type"]=="Pace"]
	#pace
	for i in range(len(overtypes)):
		cut = testpace[testpace['over_type']==overtypes[i]]
		cutballs = cut["runs_off_bat"].to_list()
		sumtaken = 0
		hitstaken = []
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
					sumtaken = sumtaken+variable
					return int(variable)
				else:
					return 0

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
			#print("GOOD - batter data generated correctly  ", testbatter)
			batter.append([x,o,t,th,f,fi,s,e,w])
		else:
			print("BAD  - weird thing happened             ", testbatter)	
	#spin
	testspin = test[test["bowler_type"]=="Spin"]
	for i in range(len(overtypes)):
		cut = testspin[testspin['over_type']==overtypes[i]]
		cutballs = cut["runs_off_bat"].to_list()
		sumtaken = 0
		hitstaken = []
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
					sumtaken = sumtaken+variable
					return int(variable)
				else:
					return 0

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
			#print("GOOD - batter data generated correctly  ", testbatter)
			batter.append([x,o,t,th,f,fi,s,e,w])
		else:
			print("BAD  - weird thing happened             ", testbatter)	
	finalbatterdata.append(batter)

for x in finalbatterdata:
	if x[1][0]=='-' and x[4][0]!='-':
		x[1]=x[4]
	if x[4][0]=='-' and x[1][0]!='-':
		x[4]=x[1]
	if x[2][0]=='-' and x[5][0]!='-':
		x[2]=x[5]
	if x[5][0]=='-' and x[2][0]!='-':
		x[5]=x[2]
	if x[3][0]=='-' and x[6][0]!='-':
		x[3]=x[6]
	if x[6][0]=='-' and x[3][0]!='-':
		x[6]=x[3]

for x in finalbatterdata:
	if x[1][0]=='-':
		if x[2][0]!='-':
			x[1]=x[2]
		else:
			x[1]=x[3]
	if x[4][0]=='-':
		if x[5][0]!='-':
			x[4]=x[5]
		else:
			x[4]=x[6]
	if x[2][0]=='-':
		if x[3][0]!='-':
			x[2]=x[3]
		else:
			x[2]=x[1]	
	if x[5][0]=='-':
		if x[6][0]!='-':
			x[5]=x[6]
		else:
			x[5]=x[4]
	if x[3][0]=='-':
		if x[2][0]!='-':
			x[3]=x[2]
		else:
			x[3]=x[1]	
	if x[6][0]=='-':
		if x[5][0]!='-':
			x[6]=x[5]
		else:
			x[6]=x[4]

finalbatterdataframe = pd.DataFrame(finalbatterdata)
finalbatterdataframe.to_csv("testHundoBatters.csv")
