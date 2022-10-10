import pandas as pd
import numpy as np
tournament_file = pd.read_csv("2022TheHundred.csv")
bowler_file = pd.read_csv("2022HundoBowlers.csv")
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

finaldata = []
print(spincounts,pacecounts)
asdf = final_data_sheet[final_data_sheet["bowler"]=="RA Reifer"]
print(asdf)
asdf = asdf[asdf["over_type"]=="1PP"]
print(asdf["runs_off_bat"].to_list())
for testbowler in bowler_dict.keys():
	bowler = [testbowler]
	test = final_data_sheet[final_data_sheet["bowler"]==testbowler]
	testtype = bowler_dict[testbowler]
	for i in range(len(overtypes)):
		cut = test[test['over_type']==overtypes[i]]
		cutballs = cut["runs_off_bat"].to_list()
		sumtaken = 0
		if len(cutballs)>0:
			x = cutballs.count(0)/len(cutballs)
			x = x-spindotpcts[i] if testtype == "Spin" else x-pacedotpcts[i]
			x = x*2
			x = x+spindotpcts[i] if testtype == "Spin" else x+pacedotpcts[i]
			x = x*(108-sumtaken)
			x = round(x,0)
			if x<0:
				x=0
			sumtaken = sumtaken+x
			if len(cutballs)-cutballs.count(0)>0:
				w = cutballs.count("W")/(len(cutballs)-cutballs.count(0))
				w = w*(108-sumtaken)
				w = round(w,0)
				sumtaken = sumtaken+w
			else:
				w = 0
			
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")>0:
				s = cutballs.count(6)/(len(cutballs)-cutballs.count(0)-cutballs.count("W"))
				s = s*(108-sumtaken)
				s = round(s,0)
				sumtaken = sumtaken+s
			else:
				s = 0
			
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6):
				f = cutballs.count(4)/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6))
				f = f*(108-sumtaken)
				f = round(f,0)
				sumtaken = sumtaken+f
			else:
				f = 0
			
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)>0:
				o = cutballs.count(1)/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4))
				o = o*(108-sumtaken)
				o = round(o,0)
				sumtaken = sumtaken+o
			else:
				o = 0
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)>0:
				e = cutballs.count("E")/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1))
				e = e*(108-sumtaken)
				e = round(e,0)
				sumtaken = sumtaken+e
			else:
				e = 0
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E")>0:
				t = cutballs.count(2)/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E"))
				t = t*(108-sumtaken)
				t = round(t,0)
				sumtaken = sumtaken+t
			else:
				t = 0
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E")-cutballs.count(2)>0:
				th = cutballs.count(3)/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E")-cutballs.count(2))
				th = th*(108-sumtaken)
				th = round(th,0)
				sumtaken = sumtaken+th
			else:
				th = 0
			if len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E")-cutballs.count(2)-cutballs.count(3)>0:
				fi = cutballs.count(5)/(len(cutballs)-cutballs.count(0)-cutballs.count("W")-cutballs.count(6)-cutballs.count(4)-cutballs.count(1)-cutballs.count("E")-cutballs.count(2)-cutballs.count(3))
				fi = fi*(108-sumtaken)
				fi = round(fi,0)
				sumtaken = sumtaken+fi
			else:
				fi = 0
			
		else:
			x = o = t = f = s = e = w = th = fi = "-"
			sumtaken = 108
		
		if sumtaken==108:
			print("GOOD - bowler data generated correctly  ", testbowler)
			bowler.append([x,o,t,th,f,fi,s,e,w])
		else:
			print("BAD  - weird thing happened             ", testbowler)
	finaldata.append(bowler)
finaldataframe = pd.DataFrame(finaldata)
finaldataframe["team"] = bowler_file["team"]
finaldataframe["type"] = bowler_file["type"]
print(finaldataframe.head(10))
	
