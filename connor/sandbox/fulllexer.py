import ply.lex as lex
from ply.lex import TOKEN
import sys

class Lexer(object):
  ### Reserved keywords ###
  # These are searched when identifiers are matched
  reserved = {
    'bool'         : 'BOOL',
    'break'        : 'BREAK',
    'case'         : 'CASE',
    'char'         : 'CHAR',
    'class'        : 'CLASS',
    'const'        : 'CONST',
    'continue'     : 'CONTINUE',
    'default'      : 'DEFAULT',
    'do'           : 'DO',
    'double'       : 'DOUBLE',
    'else'         : 'ELSE',
    'false'        : 'FALSE',
    'float'        : 'FLOAT',
    'for'          : 'FOR',
    'if'           : 'IF',
    'int'          : 'INT',
    'long'         : 'LONG',
    'private'      : 'PRIVATE',
    'public'       : 'PUBLIC',
    'return'       : 'RETURN',
    'short'        : 'SHORT',
    'static_cast'  : 'SCAST',
    'struct'       : 'STRUCT',
    'switch'       : 'SWITCH',
    'this'         : 'THIS',
    'true'         : 'TRUE',
    'void'         : 'VOID',
    'while'        : 'WHILE'
  }

  ### Single Character Literals ###
  literals = [
    ':', ',', '[', ']', '(', ')', '&', '=',
    '{', '}', ';', '?', '|', '^', '<', '>',
    '+', '-', '*', '/', '%', '.', '!', '~',
    "'", '"'
  ]

  ### Multi Character Literals ###
  mc_literals = [
    'SRES',    # scope resolution operator (::)
    'MULEQ',   # multiply assign operator (*=)
    'DIVEQ',   # divide assign operator (/=)
    'MODEQ',   # mod assign operator (%=)
    'ADDEQ',   # add assign operator (+=)
    'SUBEQ',   # subtract assign operator (-=)
    'LOR',     # logical or operator (||)
    'LAND',    # logical and operator (&&)
    'EQ',      # relational equality operator (==)
    'NEQ',     # relational negated equality operator (!=)
    'LEQ',     # relational less than or equal operator (<=)
    'GEQ',     # relational greater than or equal operator (>=)
    'LSHIFT',  # left bit shift operator (<<)
    'RSHIFT',  # right bit shift operator (>>)
    'INC',     # increment operator (++)
    'DEC'      # decrement operator (--)
  ]

  ### Tokens ###
  tokens = [
    'SCON',     # string literal
    'ID',       # identifier
    'ICON',     # integer literal
    'CCON',     # character literal
    'FCON'      # floating literal
  ] + reserved.values() + mc_literals

  ##
  ## TOKEN DEFINITIONS
  ##

  ### Partial Match Definitions ###
  decimal_literal     = r'([1-9][0-9]*)'
  octal_literal       = r'(0[0-7]*)'
  hexadecimal_literal = r'((0x|0X)[0-9a-fA-F]+)'
  escape_sequence     = r'(\\\'|\\"|\\\\|\\n|\\t)'
  fractional_constant = r'((([0-9]+)?\.[0-9]+)|([0-9]+\.))'
  exponent_part       = r'((e|E)(\+|-)[0-9]+)'

  ### Multi Character Literals ###
  t_SRES   = r'::'
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
  t_INC    = r'\+\+'
  t_DEC    = r'--'

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

  ##
  ## LEXER FUNCTIONS
  ##

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