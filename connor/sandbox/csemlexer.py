import ply.lex as lex
from ply.lex import TOKEN
import sys

class Lexer(object):
  reserved = {
    'char'     : 'CHAR',
    'float'    : 'FLOAT',
    'double'   : 'DOUBLE',
    'int'      : 'INT',
    'if'       : 'IF',
    'else'     : 'ELSE',
    'while'    : 'WHILE',
    'do'       : 'DO',
    'for'      : 'FOR',
    'continue' : 'CONTINUE',
    'break'    : 'BREAK',
    'return'   : 'RETURN'
  }

  literals = [
    ';', ',', '[', ']', '}', '{', '(', ')',
    ':', '<', '>', '!', '=', '*', '/', '%',
    '+', '-'
  ]

  mc_literals = [
    'EQ',     # relational equality operator (==)
    'NEQ',    # relational non equality operator (!=)
    'LEQ',    # less than or equal to (<=)
    'GEQ',    # greater than or equal to (>=)
    'LAND',   # logical and (&&)
    'LOR',    # logical or (||)
    'ADDEQ',  # add assign (+=)
    'SUBEQ',  # subtract assign (-=)
    'MULEQ',  # multiply assign (*=)
    'DIVEQ',  # divide assign (/=)
    'MODEQ',  # mod assign (%=)
    'LSHIFT', # left shift (<<)
    'RSHIFT'  # right shift (>>)
  ]

  tokens = [
    'SCON',   # string literal
    'ID',     # identifier
    'ICON',   # integer literal
    'CCON',   # character literal
    'FCON'    # floating literal
  ] + reserved.values() + mc_literals

  decimal_literal     = r'([1-9][0-9]*)'
  octal_literal       = r'(0[0-7]*)'
  hexadecimal_literal = r'((0x|0X)[0-9a-fA-F]+)'
  escape_sequence     = r'(\\\'|\\"|\\\\|\\n|\\t)'
  fractional_constant = r'((([0-9]+)?\.[0-9]+)|([0-9]+\.))'
  exponent_part       = r'((e|E)(\+|-)[0-9]+)'

  t_MULEQ  = r'\*='
  t_DIVEQ  = r'/='
  t_MODEQ  = r'%='
  t_ADDEQ  = r'\+='
  t_SUBEQ  = r'-='
  t_LOR    = r'\|\|'
  t_LAND   = r'&&'
  t_EQ     = r'=='
  t_NEQ    = r'!='
  t_LEQ    = r'<='
  t_GEQ    = r'>='
  t_LSHIFT = r'<<'
  t_RSHIFT = r'>>'

  # SCON
  @TOKEN(r'"(' + escape_sequence + r'|[^"\\\n])*"')
  def t_SCON(self, t):
    if t.value:
      t.value = t.value[1:-1]
    return t

  # ID
  def t_ID(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.reserved.get(t.value, 'ID')
    return t

  # ICON
  @TOKEN(decimal_literal + r'|' + octal_literal + r'|' + hexadecimal_literal)
  def t_ICON(self, t):
    t.value = int(t.value) # to do: handle octal and hex cases
    return t

  # CCON
  @TOKEN(r"'(" + escape_sequence + r"|[^'\\\n])+'")
  def t_CCON(self, t):
    t.value = t.value[1:-1]
    return t

  # FCON
  @TOKEN(r'(' + fractional_constant + exponent_part + r'?)|([0-9]+' + exponent_part + r')')
  def t_FCON(self, t):
    t.value = float(t.value) # to do: handle exp cases (will it automatically?)
    return t

  t_ignore = ' \t'

  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_error(self, t):
    print 'error'
    t.lexer.skip(1)

  def build(self, **kwargs):
    self.lexer = lex.lex(module=self, **kwargs)

  def input(self, data):
    self.lexer.input(data)

  def __iter__(self):
    return iter(self.lexer)

  def test(self, data):
    self.input(data)
    while True:
      token = self.lexer.token()
      if not token:
        break
      print token
#################################################################

##################
# For testing purposes:
#
#

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Please provide an input file.'
    exit()
    
  fin = open(sys.argv[1])
  l = Lexer()
  l.build()
  l.test(fin.read())