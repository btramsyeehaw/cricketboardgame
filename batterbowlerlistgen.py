import pandas as pd
import numpy as np
tournament_file = pd.read_csv("IPL2022.csv")
file_prefix = "IPL2022"


longstrikerlist = tournament_file['striker'].to_list()
strikerlist = [*set(longstrikerlist)]
strikerlist.remove('striker')
strikerlist.sort()
strikerlistdf = pd.DataFrame()
strikerteamlist = []

for x in strikerlist:
	for i in range(len(longstrikerlist)):
		if longstrikerlist[i]==x:
			strikerteamlist.append(tournament_file["batting_team"].to_list()[i])
			break
strikerlistdf["striker"] = strikerlist
strikerlistdf["team"] = strikerteamlist
strikerlistdf.to_csv(file_prefix+"batters.csv")
print(len(strikerlistdf),"batters added to list")

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
bowlerlistdf.to_csv(file_prefix+"bowlers.csv")
print(len(bowlerlistdf),"bowlers added to list")
