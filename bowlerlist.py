import pandas as pd
import numpy as np
tournament_file = pd.read_csv("2022TheHundred.csv")

longbowlerlist = tournament_file['bowler'].to_list()
bowlerlist = [*set(longbowlerlist)]
bowlerlist.remove('bowler')
bowlerlist.sort()
bowlerlistdf = pd.DataFrame()
bowlerteamlist = []

for x in bowlerlist:
	for i in range(len(longbowlerlist)):
		if longbowlerlist[i]==x:
			bowlerteamlist.append(tournament_file["bowling_team"].to_list()[i])
			break
bowlerlistdf["bowler"] = bowlerlist
bowlerlistdf["team"] = bowlerteamlist
bowlerlistdf.to_csv("2022HundoBowlers.csv")
print(len(bowlerlistdf),"bowlers added to list")
