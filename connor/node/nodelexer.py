import ply.lex as lex

class Lexer(object):
  reserved = {}

  tokens = ('ID', 'NUM')

  literals = ('+', '-', '(', ')')

  def t_ID(self, t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = 'ID'
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

def main():
  lexer = Lexer()
  lexer.build()
  lexer.input('5 + 7')
  for token in lexer:
    print token
  print 'done.'

if __name__ == '__main__':
  main()