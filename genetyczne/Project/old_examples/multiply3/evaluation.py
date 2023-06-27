def calculate_score(Input, Output, Expected, Terminated):
	Expected = Expected[0]
	if Terminated:
		return 0
	if len(Output) != 1:
		return 1
	val = Output[0]
	if isinstance(val, str):
		return 2
	if float(val) == float(Expected):
		return 10
	if isinstance(Input[0], str) or isinstance(Input[1], str) or isinstance(Input[2], str):
        	return 2
	if val == float(Input[0])*float(Input[1]) or val == float(Input[0])*float(Input[2]) or val == float(Input[2])*float(Input[1]):
		return 8
	return max(3, 7-abs(val - Expected))