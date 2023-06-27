from header import *
scan=input
def input():
	x=scan()
	try:
		return int(x)
	except:
		try:
			return float(x)
		except:
			return x
print(calcexpr(input(),instr(instr(instr("EEEEE",4,"DDDD"),8,instr(5,calcexpr(1,0.1,"DDDD"),instr(0.5,"DDDD",0.3))),input(),calcexpr(input(),0.5,input())),"A"))
