def calculate_score(Input, Output, Expected, Terminated):
	if Terminated:
		return 0
	i = Input[0]
	if len(Output) == int(i):
		return 5
	if len(Output) > 0:
		if len(Output) <= 2*i:
			return 2
		return 1
	return 3