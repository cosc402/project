#--------------------------------------------
# vislexer.py
#
# Specifies the lexical analyzer.
#--------------------------------------------

import ply.lex as lex

class Lexer(object):

  reserved = {
    'int'    : 'INT',
    'double' : 'DOUBLE',
    'float'  : 'FLOAT',
    'char'   : 'CHAR',
    'bool'   : 'BOOL',
    'cout'   : 'COUT'
  }

  tokens = [
    'ID', 'NUM', 'CHARACTER', 'INSERT'
  ] + list(reserved.values())

  literals = [
    '=', '+', '-', '*', '/', '(', ')', ';'
  ]

  # Token Definitions

  t_CHARACTER = "'[a-zA-Z]'"
  t_INSERT = r'<<'

  def t_ID(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.reserved.get(t.value,'ID')
    return t

  def t_NUM(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

  t_ignore = ' \t'

  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_error(self, t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

  def build(self, **kwargs):
    self.lexer = lex.lex(module=self, **kwargs)

  def input(self, data):
    self.lexer.input(data)

  def __iter__(self):
    return iter(self.lexer)