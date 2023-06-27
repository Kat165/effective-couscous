import ply.lex as lex
import ply.yacc as yacc


# -------TOKENS-------
tokens = [
    'FLOATNUMBER',
    'INTNUMBER',
    'TEXT',

    'ELIF',
    'ELSE',
    'FALSE',
    'IF',
    'TRUE',
    'WHILE',

    'CALCEXPR',
    'CALCLOGICALEXPR',
    'INSTR',

    'NL',

    'BLOCK_END',
    
    'OUTPUT',
    'INPUT'
]

literals = "()[]:,."

def t_FLOATNUMBER(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTNUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


t_ELIF = r'elif'
t_ELSE = r'else'
t_FALSE = r'False'
t_IF = r'if'
t_TRUE = r'True'
t_WHILE = r'while'

t_OUTPUT = r'output'
t_INPUT = r'input'

t_CALCEXPR = 'calcexpr'
t_CALCLOGICALEXPR = 'calclogicalexpr'
t_INSTR = 'instr'

t_TEXT = r'\"[^\n\"]*\"'

t_BLOCK_END = r'\$'

t_ignore = ' \t'


def t_NL(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    with open('output.txt', 'w') as output_file:
        output_file.write("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# --------INDENTS-------------
indents = 0


# --------GRAMMAR-------------

start = 'start'


def p_error(p):
    if not p:
        message = "EOF error"
    else:
        message = "Parsing error, wrong token:" + str(p.value) + "\nin line:" + str(int((p.lineno+1)/2)) + "\nat position: " + str(p.lexpos)
    print (message)
    with open('output.txt', 'w') as output_file:
        output_file.write(message)


def p_start(p):
    '''
    start : INSTRUCTIONS_SET
    '''
    p[0] = str(p[1])
    if len(p) > 2:
        for i in range(len(p)-2):
            p[0] += str(p[i+2])

def p_instructionsset(p):
    '''
    INSTRUCTIONS_SET : INSTRUCTION NL
        | INSTRUCTIONS_SET INSTRUCTION NL
    '''
    p[0] = str(p[1])
    if len(p) > 2:
        for i in range(len(p)-2):
            p[0] += str(p[i+2])

def p_instruction(p):
    '''
    INSTRUCTION : INSTR '(' EXPRESSION ',' EXPRESSION ',' EXPRESSION ')'
        | IF_STATEMENT
        | WHILE_STATEMENT
        | OUTPUT '(' EXPRESSION ')'
    '''
    global indents
    tabs = "    " * indents
    if len(p) == 5:
        p[0] = tabs + "print" + p[2] + p[3] + p[4]
    else:
        p[0] = tabs + str(p[1])
        if len(p) > 2:
            p[0] += p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]


def p_logicalexpression(p):
    '''
    LOGICALEXPRESSION : TRUE
        | FALSE
        | TEXT
        | INTNUMBER
        | FLOATNUMBER
        | CALCLOGICALEXPR '(' EXPRESSION ',' EXPRESSION ',' EXPRESSION ')'
        | CALCLOGICALEXPR '(' LOGICALEXPRESSION ',' EXPRESSION ',' EXPRESSION ')'
        | CALCLOGICALEXPR '(' EXPRESSION ',' LOGICALEXPRESSION ',' EXPRESSION ')'
        | CALCLOGICALEXPR '(' LOGICALEXPRESSION ',' LOGICALEXPRESSION ',' EXPRESSION ')'
    '''
    p[0] = str(p[1])
    if p[0] == 'True':
        p[0] = '1'
    elif p[0] == 'False':
        p[0] = '0'

    if len(p) > 2:
        for i in range(len(p)-2):
            p[0] += str(p[i+2])


def p_whilestatement(p):
    '''
    WHILE_STATEMENT : WHILE LOGICALEXPRESSION ':' add_indent NL INSTRUCTIONS_SET BLOCK_END remove_indent
    '''
    p[0] = p[1] + " " + p[2] + p[3] + p[5] + p[6]


def p_ifstatement(p):
    '''
    IF_STATEMENT : IF IF_BODY
    '''
    p[0] = str(p[1])
    p[0] += ' '
    if len(p) > 2:
        for i in range(len(p)-2):
            p[0] += str(p[i+2])


def p_ifbody(p):
    '''
    IF_BODY : LOGICALEXPRESSION ':' add_indent NL INSTRUCTIONS_SET BLOCK_END remove_indent
        | LOGICALEXPRESSION ':' add_indent NL INSTRUCTIONS_SET remove_indent ELIF IF_BODY
        | LOGICALEXPRESSION ':' add_indent NL INSTRUCTIONS_SET remove_indent ELSE ':' add_indent NL INSTRUCTIONS_SET BLOCK_END remove_indent
    '''
    global indents
    if len(p) == 8:
        p[0] = p[1] + p[2] + p[4] + p[5]
    elif len(p) == 9:
        p[0] = p[1] + p[2] + p[4] + p[5]
        tabs = "    " * indents
        p[0] += tabs + p[7] + ' ' + p[8]
    else:
        p[0] = p[1] + p[2] + p[4] + p[5]
        tabs = "    " * indents
        p[0] += tabs + p[7] + p[8] + p[10] + p[11]

def p_expression(p):
    '''
    EXPRESSION : CALCEXPR '(' EXPRESSION ',' EXPRESSION ',' EXPRESSION ')'
        | INTNUMBER
        | FLOATNUMBER
        | TEXT
        | INSTR '(' EXPRESSION ',' EXPRESSION ',' EXPRESSION ')'
        | INPUT '(' ')'
    '''
    p[0] = str(p[1])
    if len(p) > 2:
        for i in range(len(p)-2):
            p[0] += str(p[i+2])

def p_add_indent(p):
    "add_indent : "
    global indents
    indents += 1

def p_remove_indent(p):
    "remove_indent : "
    global indents
    indents -= 1

# ---------END----------------

def transform_program(data):
    parser = yacc.yacc()
    return parser.parse(data, lexer=lexer)