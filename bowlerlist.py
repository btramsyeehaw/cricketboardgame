import pandas as pd
import numpy as np
tournament_file = pd.read_csv("2022TheHundred.csv")

bowlerlist = [*set(tournament_file['bowler'].to_list())]
bowlerlist.remove('bowler')
bowlerlist.sort()
bowlerlistdf = pd.DataFrame(bowlerlist)
bowlerlistdf.to_csv("2022HundoBowlers.csv")
print(len(bowlerlistdf),"bowlers added to list")