file = open("README.txt")
targetfile = ("ICricketWC2022groupset.csv")
matches_to_collate = []
def addmatchtofile(matchid):
	f = open(targetfile,"a")
	z = open(matchid+".csv")
	for con in z:
		f.write(con)
for x in file:
	x=x.replace("\n", "")
	y = x.split("-")
	#member_countries = ["India","England","SouthAfrica","Pakistan","NewZealand","Australia","WestIndies","SriLanka", "Bangladesh","Afghanistan","Zimbabwe","Ireland"]
	WCqualifiers = ["India","Pakistan","Australia","England","SouthAfrica","NewZealand","Afghanistan","SriLanka","Bangladesh","Netherlands","Ireland","Zimbabwe"]
	try:
	#if y[3]=="international":
		if int(y[0])>2020:
			z = y[7].split("vs")			
			if z[0].replace(" ","") in WCqualifiers and z[1].replace(" ","") in WCqualifiers:
				matches_to_collate.append(y[6].replace(" ",""))
				print(z[0],z[1],y[1],y[2])
	except:
		print("error")
for match in matches_to_collate:
	addmatchtofile(match)
	print(match,"added")