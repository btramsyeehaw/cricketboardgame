def add_pre_to_six_rep(sixrep,prefix):
	text = ""
	for i in range(len(sixrep)):
		text=str(int(sixrep[i])+1)
	if len(text)==3:
		return text
	if len(text)==2:
		return prefix+text
	if len(text)==1:
		return prefix+prefix+text

print(add_pre_to_six_rep("366","1"))