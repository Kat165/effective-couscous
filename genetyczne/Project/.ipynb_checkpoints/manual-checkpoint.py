#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pickle
import sys
from copy import deepcopy
from io import StringIO
import os
import time
import string
from func_timeout import FunctionTimedOut, func_timeout
from multiprocessing import Process, Pipe, cpu_count
import gc

from parser import transform_program


# In[2]:


Population = 1000 # Number of programs in population
InitialMaxDepth = 10 # >=5
TournamentSize = int(Population*0.1)+ 1
# ProgramVariables = 10 # number of variables a program can use [currently no effect]
ParsToCrossover = 1 #
ProgramsToMutate = 1 # 
MaxExecutionTime = 0.1 # time in seconds
trees_type_split = 0
MaxOutputs = 100
save_programs_on_stop = False
load_programs_on_start = False
save_on_next_phase = False

input_filename = "input.txt"
expected_filename = "expected.txt"
evaluating_function = None

integers = random.sample(range(-100, 100), 100)
floats = [round(random.uniform(-100, 100), 4) for x in range(100)]
strings = [ ''.join(random.choice(string.ascii_letters) for i in range(random.randint(1,10))) for i in range(99)]
strings.append('')

coresAvaible = int(cpu_count())//2 + int(cpu_count())%2


# In[3]:


productionsDepth = {
    "INSTRUCTIONS_SET": [3, 4],
    "INSTRUCTION": [2, 6, 5, 2],
    "LOGICALEXPRESSION": [1, 1, 1, 1, 1, 2, 2, 2, 2],
    "WHILE_STATEMENT": [4],
    "IF_STATEMENT": [5],
    "IF_BODY": [4, 5, 4],
    "EXPRESSION": [2, 1, 1, 1, 2, 1]
}


# In[4]:


transitionLength = {
    "INSTRUCTIONS_SET": [2, 3],
    "INSTRUCTION": [8, 1, 1, 4],
    "LOGICALEXPRESSION": [1, 1, 1, 1, 1, 8, 8, 8, 8],
    "WHILE_STATEMENT": [6],
    "IF_STATEMENT": [2],
    "IF_BODY": [5, 6, 9],
    "EXPRESSION": [8, 1, 1, 1, 8, 3]
}


# In[5]:


TypeIndex = {
    "INSTRUCTIONS_SET": 0,
    "INSTRUCTION": 1,
    "LOGICALEXPRESSION": 2,
    "WHILE_STATEMENT": 3,
    "IF_STATEMENT": 4,
    "IF_BODY": 5,
    "EXPRESSION": 6,
    "PROGRAM": 7,
    "TEXT": 8,
    "FLOATNUMBER": 9,
    "INTNUMBER": 10,
    "FALSE": 11,
    "TRUE": 12,
    "CALCEXPR": 13,
    "CALCLOGICALEXPR": 14,
    "INSTR": 15,
    "BLOCK_END": 16,
    "NL": 17,
    "ELIF": 18,
    "ELSE": 19,
    "IF": 20,
    "WHILE": 21,
    "LP": 22,
    "RP": 23,
    "COLON": 24,
    "COMA": 25,
    "OUTPUT": 26,
    "INPUT": 27
}


# In[6]:


def SelectProductionNumber(node_type, max_depth, full_trees=False):
    depths = productionsDepth[node_type]
    possible_rules = 0
    for i in range(len(depths)):
        if depths[i] <= max_depth and (not full_trees or max_depth == 1 or depths[i] > 1):
            possible_rules += 1
    choosen = random.randint(0, possible_rules-1)
    rule_number = -1
    for i in range(len(depths)):
        if depths[i] <= max_depth and (not full_trees or max_depth == 1 or depths[i] > 1):
            rule_number +=1
            if rule_number==choosen:
                return i


# In[7]:


def randomint():
    return random.choice(integers)


# In[8]:


def randomfloat():
    return random.choice(floats)


# In[9]:


def randomstring():
    return random.choice(strings)


# In[10]:


class NL():
    name = "NL"
    val = "\n"
    def __str__(self):
        return self.val


# In[11]:


class INTNUMBER():
    name = "INTNUMBER"
    def __init__(self):
        self.val = randomint()
    def __str__(self):
        return str(self.val)


# In[12]:


class FLOATNUMBER():
    name = "FLOATNUMBER"
    def __init__(self):
        self.val = randomfloat()
    def __str__(self):
        return str(self.val)


# In[13]:


class TEXT():
    name = "TEXT"
    def __init__(self):
        self.val = "\"" + randomstring() + "\""
    def __str__(self):
        return self.val


# In[14]:


class BLOCK_END():
    name = "BLOCK_END"
    val = "$"
    def __str__(self):
        return self.val


# In[15]:


class INSTR():
    name = "INSTR"
    val = "instr"
    def __str__(self):
        return self.val    


# In[16]:


class CALCEXPR():
    name = "CALCEXPR"
    val = "calcexpr"
    def __str__(self):
        return self.val    


# In[17]:


class CALCLOGICALEXPR():
    name = "CALCLOGICALEXPR"
    val = "calclogicalexpr"
    def __str__(self):
        return self.val    


# In[18]:


class WHILE():
    name = "WHILE"
    val = "while"
    def __str__(self):
        return self.val    


# In[19]:


class TRUE():
    name = "TRUE"
    val = "True"
    def __str__(self):
        return self.val    


# In[20]:


class FALSE():
    name = "FALSE"    
    val = "False"
    def __str__(self):
        return self.val    


# In[21]:


class IF():
    name = "IF"
    val = "if"
    def __str__(self):
        return self.val   


# In[22]:


class ELSE():
    name = "ELSE"
    val = "else"
    def __str__(self):
        return self.val  


# In[23]:


class ELIF():
    name = "ELIF"
    val = "elif"
    def __str__(self):
        return self.val


# In[24]:


class COMA():
    name = "COMA"
    val = ","
    def __str__(self):
        return self.val


# In[25]:


class COLON():
    name = "COLON"
    val = ":"
    def __str__(self):
        return self.val


# In[26]:


class LP():
    name = "LP"
    val = "("
    def __str__(self):
        return self.val


# In[27]:


class RP():
    name = "RP"
    val = ")"
    def __str__(self):
        return self.val


# In[28]:


class OUTPUT():
    name = "OUTPUT"
    val = "output"
    def __str__(self):
        return self.val


# In[29]:


class INPUT():
    name = "INPUT"
    val = "input"
    def __str__(self):
        return self.val


# In[30]:


class EXPRESSION:
    name = "EXPRESSION"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = CALCEXPR()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = EXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
            case 1:
                self.children[0] = INTNUMBER()
            case 2:
                self.children[0] = FLOATNUMBER()
            case 3:
                self.children[0] = TEXT()
            case 4:
                self.children[0] = INSTR()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = EXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
            case 5:
                self.children[0] = INPUT()
                self.children[1] = LP()
                self.children[2] = RP()
        
    def __str__(self):
        self.string = ""
        for i in self.children:
            self.string += str(i)
        return self.string   


# In[31]:


class LOGICALEXPRESSION:
    name = "LOGICALEXPRESSION"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = TRUE()
            case 1:
                self.children[0] = FALSE()
            case 2:
                self.children[0] = TEXT()
            case 3:
                self.children[0] = INTNUMBER()
            case 4:
                self.children[0] = FLOATNUMBER()
            case 5:
                self.children[0] = CALCLOGICALEXPR()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = EXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
            case 6:
                self.children[0] = CALCLOGICALEXPR()
                self.children[1] = LP()
                self.children[2] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = EXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
            case 7:
                self.children[0] = CALCLOGICALEXPR()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()                
            case 8:
                self.children[0] = CALCLOGICALEXPR()
                self.children[1] = LP()
                self.children[2] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
                
    def __str__(self):
        self.string = ""
        for i in self.children:
            self.string += str(i)
        return self.string   


# In[32]:


class IF_BODY:
    name = "IF_BODY"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[1] = COLON()
                self.children[2] = NL()
                self.children[3] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[4] = BLOCK_END()
            case 1:
                self.children[0] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[1] = COLON()
                self.children[2] = NL()
                self.children[3] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[4] = ELIF()
                self.children[5] = IF_BODY(max_depth-1, full_trees)
            case 2:
                self.children[0] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[1] = COLON()
                self.children[2] = NL()
                self.children[3] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[4] = ELSE()
                self.children[5] = COLON()
                self.children[6] = NL()
                self.children[7] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[8] = BLOCK_END()
        
    def __str__(self):
        self.string = ""
        if self.production_number == 0 or self.production_number == 2:
            for i in self.children:
                self.string += str(i)
            return self.string   
        else:
            return str(self.children[0]) + str(self.children[1]) + str(self.children[2]) + str(self.children[3]) + str(self.children[4]) + ' ' + str(self.children[5])


# In[33]:


class IF_STATEMENT:
    name = "IF_STATEMENT"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = IF()
                self.children[1] = IF_BODY(max_depth-1, full_trees)
        
    def __str__(self):
        return str(self.children[0]) + ' ' + str(self.children[1])


# In[34]:


class WHILE_STATEMENT:
    name = "WHILE_STATEMENT"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = WHILE()
                self.children[1] = LOGICALEXPRESSION(max_depth-1, full_trees)
                self.children[2] = COLON()
                self.children[3] = NL()
                self.children[4] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[5] = BLOCK_END()
                
        
    def __str__(self):
        self.string = str(self.children[0]) + ' '
        for i in self.children[1:]:
            self.string += str(i)
        return self.string


# In[35]:


class INSTRUCTION:
    name = "INSTRUCTION"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = INSTR()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = COMA()
                self.children[4] = EXPRESSION(max_depth-1, full_trees)
                self.children[5] = COMA()
                self.children[6] = EXPRESSION(max_depth-1, full_trees)
                self.children[7] = RP()
            case 1:
                self.children[0] = IF_STATEMENT(max_depth-1, full_trees)
            case 2:
                self.children[0] = WHILE_STATEMENT(max_depth-1, full_trees)
            case 3:
                self.children[0] = OUTPUT()
                self.children[1] = LP()
                self.children[2] = EXPRESSION(max_depth-1, full_trees)
                self.children[3] = RP()
        
    def __str__(self):
        self.string = ""
        for i in self.children:
            self.string += str(i)
        return self.string   


# In[36]:


class INSTRUCTIONS_SET:
    name = "INSTRUCTIONS_SET"
    def __init__(self, max_depth, full_trees):
        self.production_number = SelectProductionNumber(self.name, max_depth, full_trees)
        self.children = [None] * transitionLength[self.name][self.production_number]
        
        match self.production_number:
            case 0:
                self.children[0] = INSTRUCTION(max_depth-1, full_trees)
                self.children[1] = NL()
            case 1:
                self.children[0] = INSTRUCTIONS_SET(max_depth-1, full_trees)
                self.children[1] = INSTRUCTION(max_depth-1, full_trees)
                self.children[2] = NL()
        
    def __str__(self):
        self.string = ""
        for i in self.children:
            self.string += str(i)
        return self.string   


# In[37]:


class PROGRAM:
    name = "PROGRAM"
    def __init__(self, max_depth, full_trees):
        self.children = [0]
        self.children[0] = INSTRUCTIONS_SET(max_depth-2, full_trees)
        
    def __str__(self):
        self.string = ""
        for i in self.children:
            self.string += str(i)
        return self.string   


# In[38]:


def crossover(a, b):
    a_indexes = []
    b_indexes = []
    for i in range(len(TypeIndex)):
        a_indexes.append([])
        b_indexes.append([])
    
    def fill_indexes_dfs(indexes, node, index):
        if TypeIndex[node.name] <= 7:
            for n in node.children:
                index = fill_indexes_dfs(indexes, n, index)
        indexes[TypeIndex[node.name]].append(index)
        index += 1
        return index
    
    fill_indexes_dfs(a_indexes, Programs[a], 0)
    fill_indexes_dfs(b_indexes, Programs[b], 0)  

    All_types_possible_to_change = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
    Actual_types_possible_to_change = []
    Weights_to_select_type = []
    for i in All_types_possible_to_change:
        if len(a_indexes[i]) > 0 and len(b_indexes[i]) > 0:
            Actual_types_possible_to_change.append(i)
            Weights_to_select_type.append(len(a_indexes[i]))
            
    Type_to_swap = random.choices(population=Actual_types_possible_to_change, weights=Weights_to_select_type)[0]
    index_in_a = random.choice(a_indexes[Type_to_swap])
    index_in_b = random.choice(b_indexes[Type_to_swap])
    
    def find_path(node, target_index, current_index):
        found = False
        path = []
        if TypeIndex[node.name] <= 7:
            for n in range(len(node.children)):
                found, current_index, path = find_path(node.children[n], target_index, current_index)
                if found:
                    path.append(n)
                    return (True, current_index, path)
        if target_index == current_index:
            return (True, current_index, path)
        current_index += 1
        return (found, current_index, path)
    
    path_to_a = find_path(Programs[a], index_in_a, 0)[2]
    path_to_a.reverse()
    path_to_b = find_path(Programs[b], index_in_b, 0)[2]
    path_to_b.reverse()
    
    def copy_node(initial_node, path):
        for i in path:
            initial_node = initial_node.children[i]
        return deepcopy(initial_node)
    
    copy_of_a = copy_node(Programs[a], path_to_a)
    copy_of_b = copy_node(Programs[b], path_to_b)

    def insert_node(initial_node, node_to_insert, path):
        for i in path[:len(path)-1]:
            initial_node = initial_node.children[i]
        initial_node.children[path[len(path)-1]] = node_to_insert
        return
    
    new_program_a = deepcopy(Programs[a])
    new_program_b = deepcopy(Programs[b])
    
    insert_node(new_program_a, copy_of_b, path_to_a)
    insert_node(new_program_b, copy_of_a, path_to_b)
    
    return new_program_a, new_program_b


# In[39]:


def mutate(a):
    a_indexes = []
    for i in range(len(TypeIndex)):
        a_indexes.append([])
        
    def fill_indexes_dfs(indexes, node, index):
        if TypeIndex[node.name] <= 7:
            for n in node.children:
                index = fill_indexes_dfs(indexes, n, index)
        indexes[TypeIndex[node.name]].append(index)
        index += 1
        return index
    
    fill_indexes_dfs(a_indexes, Programs[a], 0)
    Types_possible_to_mutate = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
    Weights_to_select_type = []
    
    for i in Types_possible_to_mutate:
        Weights_to_select_type.append(len(a_indexes[i]))
    
    Type_to_mutate = random.choices(population=Types_possible_to_mutate, weights=Weights_to_select_type)[0]
    index_to_mutate = random.choice(a_indexes[Type_to_mutate])
    
    def find_path(node, target_index, current_index):
        found = False
        path = []
        if TypeIndex[node.name] <= 7:
            for n in range(len(node.children)):
                found, current_index, path = find_path(node.children[n], target_index, current_index)
                if found:
                    path.append(n)
                    return (True, current_index, path)
        if target_index == current_index:
            return (True, current_index, path)
        current_index += 1
        return (found, current_index, path)

    path_to_index = find_path(Programs[a], index_to_mutate, 0)[2]
    path_to_index.reverse()
    
    node = Programs[a]
    for i in path_to_index:
        node = node.children[i]
        
    def find_max_depth(node):
        if TypeIndex[node.name] <= 7:
            depths = []
            for n in node.children:
                depths.append(1 + find_max_depth(n))
            return max(depths)
        else:
            return 1
    
    if Type_to_mutate <= 6:
        max_depth = find_max_depth(node)        
        node = node.__init__(max_depth-1, False)
    else:
        node = node.__init__()


# In[40]:


def save_transformed_program_as_string(program_nr, filename):
    filename += ".txt"
    with open(filename, 'w') as f:
            f.write(TransformedPrograms[program_nr])


# In[41]:


def save_transformed_program_as_py(program_nr, filename):
    filename += ".py"
    with open(filename, 'w') as f:
            f.write("from header import *\nscan=input\ndef input():\n\tx=scan()\n\ttry:\n\t\treturn int(x)\n\texcept:\n\t\ttry:\n\t\t\treturn float(x)\n\t\texcept:\n\t\t\treturn x\n" + "import sys\nout=print\nouts=0\ndef print(val):\n\tglobal outs\n\tglobal out\n\touts+=1\n\tif outs>" + str(MaxOutputs) + ":\n\t\tsys.exit()\n\tout(val)\n" +TransformedPrograms[program_nr])


# In[42]:


def save_program(filename, program):
    filename += ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(program, f, pickle.HIGHEST_PROTOCOL)


# In[43]:


def load_program(filename):
    filename += ".pkl"
    with open(filename, 'rb') as f:
        return pickle.load(f)


# In[44]:


def pick_programs(population_size, tournament_size=TournamentSize, best=True):
    new_population = list()
    
    for i in range(population_size):
        new_population.append(pick_one(min(tournament_size, Population-len(new_population)), new_population, best))
        
    return new_population


# In[45]:


def pick_one(tournament_size, exclude=[], best=True):
    to_tournament = [index for index in range(Population) if index not in exclude]
    tournament_participants = random.sample(to_tournament, tournament_size)
    participants_scores = [scores[index] for index in tournament_participants]
    wanted_score = min(participants_scores)
    if best:
        wanted_score = max(participants_scores)     
    for i in range(len(to_tournament)):
        if scores[to_tournament[i]] == wanted_score:
            return to_tournament[i]


# In[46]:


def transform_programs():
    for i in range(len(Programs)):
        TransformedPrograms[i] = transform_program(str(Programs[i]))


# In[47]:


def execute_programs():
    if multi:
        execute_multiprocess()
    else:
        execute_singleprocess()


# In[48]:


def execute_multiprocess():
    Processes = [[0] * len(InputTable) for i in range(Population)]
    for program_nr in range(len(TransformedPrograms)):
        for test_nr in range(len(InputTable)):
            Execution_terminated[program_nr][test_nr] = False
            Processes[program_nr][test_nr] = Process(target=run_program_multiprocess_only, args=("from header import *\nfor i in range(len(var)):\n\tvar[i]=0\nfrom ast import literal_eval\nInputTab=literal_eval(\""+ str(InputTable[test_nr]) +"\")\nValue_nr = 0\ndef input():\n\tglobal Value_nr\n\tglobal InputTab\n\tValue_nr+=1\n\treturn '' if len(InputTab)<=Value_nr-1 else InputTab[Value_nr-1]\n" + "import sys\nout=print\nouts=0\ndef print(val):\n\tglobal outs\n\tglobal out\n\touts+=1\n\tif outs>" + str(MaxOutputs) + ":\n\t\tsys.exit()\n\tout(val)\n" + TransformedPrograms[program_nr],Outputs[program_nr][test_nr][1]))
    
    waitTime = 1
    if MaxExecutionTime < 1:
        waitTime = MaxExecutionTime
    
    ProcessesStarted = 0
    while ProcessesStarted < len(InputTable) * Population:
        timeSlept = 0
        InProgress = []
        for i in range(min(coresAvaible, len(InputTable) * Population - ProcessesStarted)):
            InProgress.append((ProcessesStarted//len(InputTable), ProcessesStarted%len(InputTable)))
            ProcessesStarted += 1
    
        for index in range(len(InProgress)):
            Processes[InProgress[index][0]][InProgress[index][1]].start()
            
        while timeSlept < MaxExecutionTime:
            all_finished = True
            for index in range(len(InProgress)):
                if Processes[InProgress[index][0]][InProgress[index][1]].is_alive():
                    all_finished = False
                    break
            if all_finished:
                break
            timeSlept += waitTime
            time.sleep(waitTime)
        
        for index in range(len(InProgress)):
            if Processes[InProgress[index][0]][InProgress[index][1]].is_alive():
                Processes[InProgress[index][0]][InProgress[index][1]].terminate()
                Execution_terminated[InProgress[index][0]][InProgress[index][1]] = True
                
        for index in range(len(InProgress)):
            Processes[InProgress[index][0]][InProgress[index][1]].join()
            Processes[InProgress[index][0]][InProgress[index][1]].close()
        
        gc.collect()


# In[49]:


def run_program_multiprocess_only(function, sender):
    def print(val):
        sender.send(val)
    exec(function)


# In[50]:


def execute_singleprocess():
    stdout = sys.stdout
    
    for program_nr in range(len(TransformedPrograms)):
        for test_nr in range(len(InputTable)):
            sys.stdout = Outputs[program_nr][test_nr]
            Execution_terminated[program_nr][test_nr] = False
            try:
                func_timeout(MaxExecutionTime, exec, args=("from header import *\nfor i in range(len(var)):\n\tvar[i]=0\nfrom ast import literal_eval\nInputTab=literal_eval(\""+ str(InputTable[test_nr]) +"\")\nValue_nr = 0\ndef input():\n\tglobal Value_nr\n\tglobal InputTab\n\tValue_nr+=1\n\treturn '' if len(InputTab)<=Value_nr-1 else InputTab[Value_nr-1]\n"+ "import sys\nout=print\nouts=0\ndef print(val):\n\tglobal outs\n\tglobal out\n\touts+=1\n\tif outs>" + str(MaxOutputs) + ":\n\t\tsys.exit()\n\tout(val)\n" + TransformedPrograms[program_nr],))
            except (FunctionTimedOut, SystemExit):
                Execution_terminated[program_nr][test_nr] = True
            finally:
                gc.collect()
                sys.stdout = stdout
#                 print("execute", program_nr, test_nr)


# In[51]:


def clear_outputs():
    Outputs = []
    for i in range(Population):
        Outputs.append([])
    if multi:
        for i in range(Population):
            for j in range(len(InputTable)):
                Outputs[i].append(Pipe())
    else:
        for i in range(Population):
            for j in range(len(InputTable)):
                Outputs[i].append(StringIO())
    return Outputs


# In[52]:


def load_input(filepath_input = "input.txt", filepath_expected="expected.txt"):
    InputTable = []
    ExpectedValues = []
    with open(filepath_input, 'r') as file:
        while line := file.readline().split():
            for i in range(len(line)):
                try:
                    line[i] = int(line[i])
                except:
                    try:
                        line[i] = float(line[i])
                    except:
                        line[i] = str(line[i][1:len(line[i])-1])
            InputTable.append(line)
    with open(filepath_expected, 'r') as file:
        while line := file.readline().split():
            for i in range(len(line)):
                try:
                    line[i] = int(line[i])
                except:
                    try:
                        line[i] = float(line[i])
                    except:
                        line[i] = str(line[i][1:len(line[i])-1])
            ExpectedValues.append(line)
    return InputTable, ExpectedValues


# In[53]:


def load_settings(filepath = "settings.txt"):
    settings = []
    with open(filepath, 'r') as file:
        for i in range(5):
            x = file.readline().split()[0]
            if x == '-' or x == '#':
                settings.append(-1)
            else:
                settings.append(int(x))
                
        x = file.readline().split()[0]
        if x == '-' or x == '#':
            settings.append(-1)
        else:
            settings.append(float(x))
        
        for i in range(3):
            x = file.readline().split()[0]
            if x == '-' or x == '#':
                settings.append(-1)
            else:
                settings.append(x)
                
        x = file.readline().split()[0]
        if x == '-' or x == '#':
            settings.append(-1)
        else:
            settings.append(float(x))      
                
        for i in range(4):
            x = file.readline().split()[0]
            if x == '-' or x == '#':
                settings.append(-1)
            else:
                settings.append(int(x)) 
            
        s, v = file.readline().split()[:2]
        if s == '-' or s == '#':
            settings.append(-1)
        else:
            settings.append([int(s), int(v)])
        
        settings.append([])
        settings.append([])
        settings.append([])
        settings.append([])
        settings.append([])
        settings.append([])
        
        transitions = file.readline().split()
        values = file.readline().split()
        MaxOuts = file.readline().split()
        for i in range(len(transitions)):
            if transitions[i] == '-' or transitions[i] == '#':
                break
            settings[15].append(int(transitions[i]))
            settings[16].append(int(values[i]))
            settings[17].append(int(MaxOuts[i]))
        
        if len(settings[15]) > 0:
            for x in range(3):
                line = file.readline().split()[:len(settings[15])]
                for i in range(len(line)):
                    settings[18+x].append(line[i])
    
    global Population
    global InitialMaxDepth
    global TournamentSize
    global ParsToCrossover
    global ProgramsToMutate
    global MaxExecutionTime
    global input_filename
    global expected_filename
    global MaxOutputs
    global trees_type_split
    global save_programs_on_stop
    global load_programs_on_start
    global save_on_next_phase
    
    if settings[0] != -1:
        Population = settings[0]
    if settings[1] != -1:
        InitialMaxDepth = settings[1]
    if settings[2] != -1:
        TournamentSize = settings[2]
    if settings[3] != -1:
        ParsToCrossover = settings[3]
    if settings[4] != -1:
        ProgramsToMutate = settings[4]
    if settings[5] != -1:
        MaxExecutionTime = settings[5]
    if settings[6] != -1:
        input_filename = settings[6]
    if settings[7] != -1:
        expected_filename = settings[7]
    if settings[8] != -1:
        exec("from evaluation import " + settings[8] +"\nglobal evaluating_function\nevaluating_function=" + settings[8])
    if settings[9] != -1:
        trees_type_split = settings[9]
    if settings[10] != -1:
        MaxOutputs = settings[10]
    if settings[11] != -1:
        load_programs_on_start = (settings[11] != 0)
    if settings[12] != -1:
        load_programs_on_start = (settings[12] != 0)
    if settings[13] != -1:
        save_on_next_phase = (settings[13] != 0)

    return settings


# In[54]:


def reset_scores():
    return [0] * Population, [[0] * len(InputTable) for i in range(Population)]


# In[55]:


def fill_scores():
    if multi:
        for program_nr in range(len(scores)):
            for test_nr in range(len(InputTable)):
                OutputList = []
                while Outputs[program_nr][test_nr][0].poll():
                    message = Outputs[program_nr][test_nr][0].recv()
                    x = None
                    try:
                        x = int(message)
                    except:
                        try:
                            x = float(message)
                        except:
                            x = str(message)
                    OutputList.append(x)
                score = evaluating_function(InputTable[test_nr], OutputList, ExpectedValues[test_nr], Execution_terminated[program_nr][test_nr])
                testScores[program_nr][test_nr] = score
                scores[program_nr] += score
    else:
        for program_nr in range(len(scores)):
            for test_nr in range(len(InputTable)):
                OutputList = []
                for i in Outputs[program_nr][test_nr].getvalue().splitlines():
                    try:
                        x = int(i)
                    except:
                        try:
                            x = float(i)
                        except:
                            x = str(i)
                    OutputList.append(x)
                score = evaluating_function(InputTable[test_nr], OutputList, ExpectedValues[test_nr], Execution_terminated[program_nr][test_nr])
                testScores[program_nr][test_nr] = score
                scores[program_nr] += score
#                 print("fill", program_nr, test_nr)


# In[56]:


def evolve(pars_to_crossover = ParsToCrossover, programs_to_mutate = ProgramsToMutate):
    programs_to_crossover = pick_programs(2*pars_to_crossover)
    new_programs = []
    for i in range(pars_to_crossover):
        new_programs.append(crossover(programs_to_crossover[2*i], programs_to_crossover[2*i+1]))
        
    programs_to_swap = pick_programs(2*pars_to_crossover, best=False)
    for i in range(len(programs_to_swap)):
        Programs[programs_to_swap[i]] = new_programs[i//2][i%2]
            
    indexes_to_mutate = random.sample([x for x in range(0, Population) if x not in programs_to_crossover and x not in programs_to_swap], programs_to_mutate)
    for i in indexes_to_mutate:
        mutate(i)
            
    global scores
    global testScores
    global Outputs
    
    scores, testScores = reset_scores()
    Outputs = clear_outputs()
    
    transform_programs()
    execute_programs()
    fill_scores()


# In[57]:


def check_stop_condition(t, c):
    if t == None:
        return False 
    elif t == 1:
        if generation_nr >= c:
            return True
    elif t == 2:
        if max(scores) >= c:
            return True
    elif t == 3:
        if sum(scores)/len(scores) >= c:
            return True
    elif t == 4:
        x = 0
        for i in range(len(scores)):
            if scores[i] >= c:
                x += 1
        if x >= len(scores)/2:
            return True
    return False


# In[58]:


def load_next_phase():
    global phase
    global MaxOutputs
    if len(settings[15]) > phase:
        if check_stop_condition(settings[15][phase], settings[15][phase]):
            if save_on_next_phase:
                save_programs()
            InputTable, ExpectedValues = load_input(settings[18][phase], settings[19][phase])
            MaxOutputs = settings[17][phase]
            exec("from evaluation import " + settings[20][phase] +"\nglobal evaluating_function\nevaluating_function=" + settings[20][phase])
            phase += 1


# In[59]:


def save_programs():
    for i in range(Population):
        save_program("saved_programs\\P" + str(i), Programs[i])


# In[60]:


def load_programs():
    for i in range(Population):
        Programs[i] = load_program("saved_programs\\P" + str(i))


# In[61]:


if __name__ == '__main__':
    multi = None
    try:
        current_path = os.path.abspath(__file__)
        if current_path[len(current_path)-3:] == '.py':
            multi = True
    except:
        multi = False

    settings = load_settings()
    
    if trees_type_split < 0:
        trees_type_split = 0
    elif trees_type_split >1:
        trees_type_split = 1
    
    stop_type = None
    stop_value = None
    if settings[14] != -1:
        stop_type = settings[14][0]
        stop_value = settings[14][1]
    
    Programs = [None] * Population
    TransformedPrograms = [None] * Population
    InputTable, ExpectedValues = load_input()
    Execution_terminated = [[0] * len(InputTable) for i in range(Population)]
    Outputs = clear_outputs()
    scores, testScores = reset_scores()
    
    if load_programs_on_start:
        load_programs()
    else:
        for i in range(Population):
            Programs[i] = PROGRAM(InitialMaxDepth, i/Population < trees_type_split)
        
    transform_programs()
    execute_programs()
    fill_scores()
    save_transformed_program_as_py(scores.index(max(scores)),"LastBest")
    
    print(0, max(scores), scores)
    
    generation_nr = 1
    phase = 0
    
    while True:
        if check_stop_condition(stop_type, stop_value):
            if save_programs_on_stop:
                save_programs()
            break
        load_next_phase()
        evolve()
        save_transformed_program_as_py(scores.index(max(scores)),"LastBest")
        print(generation_nr, max(scores), scores)
        generation_nr += 1


# In[62]:


save_programs()


# In[ ]:




