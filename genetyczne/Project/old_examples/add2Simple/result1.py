from header import *
import sys
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
print(calcexpr(input(),input(),calcexpr(input(),"EEEEE",calcexpr(calcexpr(6.66,calcexpr(input(),input(),input()),5),instr(instr(input(),input(),6),3,input()),8))))
instr("DDDD","CCC","BB")
instr("CCC",input(),2)
instr(2,"A",1)
instr("DDDD",input(),input())
instr(1,input(),"CCC")
