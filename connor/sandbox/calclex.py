#------------------------------------------
# calclex.py
# tokenizer for a simple calculator
#------------------------------------------

import ply.lex as lex

# list of token names. MUST BE NAMED "tokens"
tokens = [
  'NUMBER',
  'PLUS',
  'MINUS',
  'TIMES',
  'DIVIDE',
  'LPAREN',
  'RPAREN'
]

# regular expressions for simple tokens. Must take the form "t_TOKENNAME"
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'

# a regular expression rule with some action code
def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

# define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  #print "I'm the newline function. I ate up {} new lines!".format(len(t.value))
  t.lexer.lineno += len(t.value)

# a string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# error handling rule
def t_error(t):
  print "Illegal character '%s'" % t.value[0]
  t.lexer.skip(1)

# build the lexer
lexer = lex.lex()

#===========================
# test it out

def main():
  data = '''
  3 + 4 * 10
  4 + 7
  '''

  # give the lexer some input
  lexer.input(data)

  # tokenize
  for tok in lexer:
    print str(tok) + 'token value: ' + str(tok.value)

if __name__ == '__main__':
  main()