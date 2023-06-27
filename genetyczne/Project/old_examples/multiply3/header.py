#!/usr/bin/env python
# coding: utf-8

# In[2]:

from math import isinf
var = [0]*10


# In[3]:


def calcexpr(a, b, action):
    a, b, action = controlValues(a, b, action)

    if type(action) == float:
        action = int(action)
    elif type(action) == str:
        action = len(action)
    action %= 5
    
    if action == 0:
        if type(a) == str:
            return a+str(b)
        else:
            if type(b) == str:
                return a+len(b)
            else:
                return a+b
    if action == 1:
        if type(a) == str:
            if type(b) == str:
                b = len(b)
            b = int(b)
            if b>=len(a):
                return ""
            else:
                return a[:len(a)-b]
        else:
            if type(b) == str:
                return a-len(b)
            else:
                return a-b
    if action == 2:
        if type(a) == str:
            if type(b) == str:
                b = len(b)
            b = int(b)
            return a*b
        else:
            if type(b) == str:
                return a*len(b)
            else:
                return a*b
    if action == 3:
        if type(a) == str:
            if type(b) == str:
                b = len(b)
            b = int(b)
            if b == 0:
                b=1
            return a[:int(len(a)/b)]
        else:
            if type(b) == str:
                if len(b)==0:
                    return a
                try:
                    return a/len(b)
                except:
                    return a//len(b)
            else:
                if b == 0:
                    return a
                return a/b
    else:
        if type(a) == str:
            if type(b) == str:
                b = len(b)
            b = int(b)
            if a=="":
                return ""
            b = b%len(a)
            if b==0:
                b=1
            return a[:int(len(a)/b)]
        else:
            if type(b) == str:
                b = len(b)
                if b==0:
                    b=1
                return a%b
            else:
                if b==0:
                    b=1
                return a%b


# In[4]:


def calclogicalexpr(a, b, action):
    a, b, action = controlValues(a, b, action)

    if type(action) == float:
        action = int(action)
    elif type(action) == str:
        action = len(action)
    action %= 10
    
    if action==0:
        return a and b
    if action==1:
        return a or b
    if action==2:
        return not a
    if action==3:
        b=(len(str(b))%2)
        a = not a
        if b==1:
            return a
        else:
            return not a
    if action==4:
        return a == b
    if action==5:
        return a!=b
    
    if type(a)!=type(b):
        if type(a)==int:
            if type(b) == str:
                b=len(b)
            else:
                b=int(b)
        elif type(a) == str:
            b = str(b)
        else:
            if type(b)==str:
                b = len(b)
    
    if action==6:
        return a>b
    if action==7:
        return a<b
    if action==8:
        return a>=b
    return a<=b


# In[5]:


def instr(a, b, action):
    a, b, action = controlValues(a, b, action)
    
    if type(action) == float:
        action = int(action)
    elif type(action) == str:
        action = len(action)
    action %= 7
    
    if type(a)==str:
        a = len(a)
    elif type(a) == float:
        a = int(a)
    a = a%len(var)
    
    if action==0:
        return var[a]
    if action==1:
        var[a]=b
        return b
    if action==2:
        return instr(a, calcexpr(var[a], b, 0), 1)
    if action==3:
        return instr(a, calcexpr(var[a], b, 1), 1)
    if action==4:
        return instr(a, calcexpr(var[a], b, 2), 1)
    if action==5:
        return instr(a, calcexpr(var[a], b, 3), 1)
    if action==6:
        return instr(a, calcexpr(var[a], b, 4), 1)

def controlValues(a, b, c):
    if isinstance(a, float):
        if isinf(a):
            a = 0
    if isinstance(b, float):
        if isinf(b):
            b = 0
    if isinstance(c, float):
        if isinf(c):
            c = 0
    
    if isinstance(a, int):
        if a > 1e+308:
            a = int(1e+308)
        elif a < -1e+308:
            a = int(-1e+308)
    if isinstance(b, int):
        if b > 1e+308:
            b = int(1e+308)
        elif b < -1e+308:
            b = int(-1e+308)
    if isinstance(c, int):
        if c > 1e+308:
            c = int(1e+308)
        elif c < -1e+308:
            c = int(-1e+308)
            
    return a, b, c

