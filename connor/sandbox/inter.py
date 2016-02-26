# -----------------------------------------------------------------------------
# inter.py
#
# C language interpreter using PLY
# -----------------------------------------------------------------------------


import symbol
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
  'ID','NUMBER','SEMICOLON','CHARACTER'
  ] + list(reserved.values())

literals = ['=','+','-','*','/', '(',')', '<']


# Tokens

t_SEMICOLON = r';'
t_CHARACTER = '\'[a-zA-Z]\''

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value,"ID")
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

# Initialize symbol table
symtab = symbol.Env()

def p_statement_assign(p):
  'statement : ID "=" expression SEMICOLON'
  # names[p[1]] = p[3]
  symtab.update(p[1], p[3])


def p_statement_declr_assign(p):
  'statement : declaration ID "=" expression SEMICOLON'
  # names[p[2]] = p[4]
  symtab.put(p[2], p[1], p[4])


def p_statement_cout(p):
  'statement : COUT "<" "<" expression SEMICOLON'
  print(p[4])


def p_statement_declr(p):
  'statement : declaration ID SEMICOLON'
  # names[p[2]] = 0
  symtab.put(p[2], p[1], 0)


def p_declaration_var(p):
  '''declaration : INT
                 | DOUBLE
                 | FLOAT
                 | CHAR
                 | BOOL'''
  p[0] = p[1]


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


def p_expression_id(p):
  "expression : ID"
  p[0] = symtab.get(p[1]).value


def p_error(p):
  if p:
      print("Syntax error at '%s'" % p.value)
  else:
      print("Syntax error at EOF")


import ply.yacc as yacc
yacc.yacc()


while True:
  try:
    s = raw_input('test > ')
    if(s == "quit()"):
      break
  except EOFError:
    break
  if not s: continue
  yacc.parse(s)
  symtab.print_table()