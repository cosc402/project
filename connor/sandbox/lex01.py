import ply.lex as lex
from ply.lex import TOKEN

tokens = [
  'ID'
]

digit        = r'([0-9])'
nondigit     = r'([_A-Za-z])'
identifier   = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

t_ignore = ' \t'

@TOKEN(identifier)
def t_ID(t):
  t.type = 'ID'
  return t

def t_error(t):
  print 'there was bad character, you fucking idiot'
  t.lexer.skip(1)

lexer = lex.lex()

#########
# test
#########

data = '''foo69 * helloworld1337'''

lexer.input(data)
for tok in lexer:
  print tok
