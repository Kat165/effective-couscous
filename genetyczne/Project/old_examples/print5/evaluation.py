def calculate_score(Input, Output, Expected, Terminated):
	Expected = Expected[0]
	if Terminated:
		return 0
	x = len(Output)
	return max(0, 5-abs(5-x))