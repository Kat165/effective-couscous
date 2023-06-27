def calculate_score(Input, Output, Expected, Terminated):
	Expected = float(Input[0]) + float(Input[1])
	if Terminated:
		return 0
	if len(Output) != 1:
		return 1
	val = Output[0]
	if isinstance(val, str):
		return 2
	if float(val) == float(Expected):
		return 5
	return 3