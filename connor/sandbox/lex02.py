###############################
# better organization via classes
#   IMPORTANT: When building a lexer from class, you should
#   construct the lexer from an instance of the CLASS, not
#   the object. This is because PLY only works properly if the
#   lexer actions are defined by bound methods.
###############################

import ply.lex as lex
from ply.lex import TOKEN

class MyLexer(object):
  # list of token names. this is always required and must be named "tokens"
  tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
    )

  # regular expression rules for simple tokens
  t_PLUS    = r'\+'
  t_MINUS   = r'-'
  t_TIMES   = r'\*'
  t_DIVIDE  = r'/'
  t_LPAREN  = r'\('
  t_RPAREN  = r'\)'

  # a regular expression rule with some action code
  def t_NUMBER(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

  # define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    # t.value is a string with some number of new line characters.
    # The length of this string will correspond to the number of
    # new line characters
    t.lexer.lineno += len(t.value)

  # ignore other whitespace
  t_ignore = ' \t'

  # error handling
  def t_error(self, t):
    print "Skipping illegal character '{}'".format(t.value[0])
    t.lexer.skip(1)

  # build the lexer
  def build(self, **kwargs):
    self.lexer = lex.lex(module=self, **kwargs)

  # tester function
  def test(self, data):
    self.lexer.input(data)
    for tok in self.lexer:
      print tok

##########################
# build the lexer and try it out

m = MyLexer()
m.build()
m.test("3 + 4")
