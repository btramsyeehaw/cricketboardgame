file = open("README.txt")
targetfile = ("2022TheHundred.csv")
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
	#WCqualifiers = ["India","Pakistan","Australia","England","SouthAfrica","NewZealand","WestIndies","Afghanistan","SriLanka","Bangladesh","Netherlands","PapuaNewGuinea","Ireland","Namibia","Scotland","Oman"]
	try:
		if y[0]=="2022":
			if True:
				z = y[7].split("vs")			
				if True:
					matches_to_collate.append(y[6].replace(" ",""))
					print(z[0],z[1],y[1],y[2])
	except:
		print("error")
for match in matches_to_collate:
	addmatchtofile(match)
	print(match,"added")