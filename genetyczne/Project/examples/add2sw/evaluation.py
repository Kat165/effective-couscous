def fun1(Input, Output, Expected, Terminated):
	if len(Output) == 0 and Terminated:
		return 0
	if len(Output) == 0:
		return 1

	x1 = float(Input[0])
	x2 = float(Input[1])
	potencially_good = []
	if x2 != 0 and x1 != 0:
		potencially_good = [x1+x2, x1*x2, x1/x2, x2/x1, x1-x2, x2-x1]
	elif x1 != 0:
		potencially_good = [x1 + x2, x1 * x2, x2 / x1, x1 - x2, x2 - x1]
	elif x2 != 0:
		potencially_good = [x1 + x2, x1 * x2, x1 / x2, x1 - x2, x2 - x1]
	else:
		potencially_good = [x1 + x2, x1 * x2, x1 - x2, x2 - x1]

	present = []
	for i in Output:
		if i in potencially_good:
			present.append(i)

	if len(present) == 0:
		return 2
	return 3

def fun2(Input, Output, Expected, Terminated):
	if len(Output) == 0 and Terminated:
		return 0
	if len(Output) == 0:
		return 1

	x1 = float(Input[0])
	x2 = float(Input[1])
	good = x1 + x2
	present = []
	for i in Output:
		if i == good:
			present.append(i)

	if len(present) == 0:
		return 2
	return 4

def fun3(Input, Output, Expected, Terminated):
	if len(Output) == 0 or Terminated:
		return 0

	x1 = float(Input[0])
	x2 = float(Input[1])
	good = x1 + x2
	present = []
	for i in Output:
		if present == good:
			present.append(i)

	if len(present) == 0:
		return 2
	return 5

def fun4(Input, Output, Expected, Terminated):
	if len(Output) == 0 or Terminated:
		return 0

	x1 = float(Input[0])
	x2 = float(Input[1])
	good = x1 + x2
	if len(Output) > 1:
		if Output[0] == good:
			return 8
		else:
			present = []
			for i in Output:
				if present in good:
					present.append(i)

			if len(present) > 0:
				return 9
			else:
				return 5
	else:
		if Output[0] == good:
			return 10
		else:
			return 6