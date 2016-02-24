# -----------------------------------------------------------------------------
# inter.py
#
# C language interpreter using PLY
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    'int'    : 'INT',
    'double' : 'DOUBLE',
    'float'  : 'FLOAT',
    'char'   : 'CHAR',
    'bool'   : 'BOOL',
    'cout'   : 'COUT',
}

tokens = [
     'NAME','NUMBER','SEMICOLON','CHARACTER',
     ] + list(reserved.values())

literals = ['=','+','-','*','/', '(',')','<']

# Tokens

t_SEMICOLON = r';'
t_CHARACTER = r'\'[a-zA-Z]\''

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,"NAME")
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()
# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression SEMICOLON'
    names[p[1]] = p[3]

def p_statement_declr_assign(p):
    'statement : declaration NAME "=" expression SEMICOLON'
    names[p[2]] = p[4]

def p_statement_expr(p):
    "statement : COUT '<' '<' expression SEMICOLON"
    print(p[4])

def p_statement_declr(p):
    'statement : declaration NAME SEMICOLON'
    names[p[2]] = 0

def p_declaration_var(p):
    '''declaration : INT
                 | DOUBLE
                 | FLOAT
                 | CHAR
                 | BOOL'''

#def p_outexpression(p):
#   "outexpression : expression '<' '<' expression"

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_character(p):
    "expression : CHARACTER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('test > ')
        if(s == "quit()"):
            break
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)

