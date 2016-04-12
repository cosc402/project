import ply.lex as lex
from ply.lex import TOKEN
import sys
from node import *

class Lexer(object):
  # t.value will have the form
  # Node('CHAR', 'char')
  # etc.
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

  # Lexer returns the literal operator as a string in t.value
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

  # The parser expects the lexical values of certain tokens to be
  # objects of type Node(token_label, token_value). That way,
  # the parser is able to interpret the value according to
  # the value's associated data type. If the parser sees a string
  # instead of a Node for a value, the parser will interpret the
  # string as a literal. For example, if t is a token, then
  # t.value is
  #
  #      int i;    ==>   Node('INT', 'int'), Node('ID', 'i')
  #      i += 5;   ==>   Node('ID', 'i'), '+=', Node('ICON', 5)
  #
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
  #
  # t.value = Node('SCON', value = string inside double quotes)
  #
  @TOKEN(r'"(' + escape_sequence + r'|[^"\\\n])*"')
  def t_SCON(self, t):
    t.value = Node('SCON', value=t.value[1:-1])
    return t

  # ID
  #
  # This pattern also matches reserved keywords. If a keyword is matched,
  # the token returned has t.type modified accordingly.
  #
  # In any case, t.value = Node(type, value = matched pattern).
  #
  def t_ID(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.reserved.get(t.value, 'ID')
    t.value = Node(t.type, value=t.value)
    return t

  # ICON
  #
  # t.value = Node('ICON', value = int(matched string))
  #
  @TOKEN(decimal_literal + r'|' + octal_literal + r'|' + hexadecimal_literal)
  def t_ICON(self, t):
    # to do: handle octal and hex cases
    t.value = Node('ICON', value=int(t.value))
    return t

  # CCON
  #
  # t.value = Node('CCON', value = string inside single quotes)
  #
  @TOKEN(r"'(" + escape_sequence + r"|[^'\\\n])+'")
  def t_CCON(self, t):
    t.value = Node('CCON', value=t.value[1:-1])
    return t

  # FCON
  #
  # t.value = Node('FCON', value = float(matched string))
  #
  @TOKEN(r'(' + fractional_constant + exponent_part + r'?)|([0-9]+' + exponent_part + r')')
  def t_FCON(self, t):
    # to do: handle exp cases (will it automatically?)
    t.value = float(t.value)
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
      print token.value
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