import pandas as pd
import numpy as np
tournament_file = pd.read_csv("ICricketWC2022set.csv")

longbowlerlist = tournament_file['striker'].to_list()
bowlerlist = [*set(longbowlerlist)]
bowlerlist.remove('striker')
bowlerlist.sort()
bowlerlistdf = pd.DataFrame()
bowlerteamlist = []

for x in bowlerlist:
	for i in range(len(longbowlerlist)):
		if longbowlerlist[i]==x:
			bowlerteamlist.append(tournament_file["batting_team"].to_list()[i])
			break
bowlerlistdf["striker"] = bowlerlist
bowlerlistdf["team"] = bowlerteamlist
bowlerlistdf.to_csv("WC2022batters.csv")
print(len(bowlerlistdf),"batters added to list")
