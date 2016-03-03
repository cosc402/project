import nodelexer
import node
import ply.yacc as yacc

class Parser(object):
  def __init__(self, toklist):
    self.tokens = toklist

  def p_stmt(self, p):
    "s : e"
    print p[1]

  def p_expr_add(self, p):
    "e : e '+' t"
    p[0] = node.Node('+', p[1], p[3])

  def p_expr_sub(self, p):
    "e : e '-' t"
    p[0] = node.Node('-', p[1], p[3])

  def p_expr_t(self, p):
    "e : t"
    p[0] = p[1]

  def p_t_paren(self, p):
    "t : '(' e ')'"
    p[0] = p[2]
    # don't create leaf nodes for the parens because they've done
    # their job in defining the value of t

  def p_t_ID(self, p):
    "t : ID"
    p[0] = node.Leaf('ID', p[1])

  def p_t_NUM(self, p):
    "t : NUM"
    p[0] = node.Leaf('NUM', p[1])

  # end of grammar #

  def p_error(self, p):
    if p:
      print("Syntax error at {}".format(p))
    else:
      print("syntax error at EOF")

  def build(self, **kwargs):
    self.parser = yacc.yacc(module=self, **kwargs)

  def parse(self, data):
    self.parser.parse(data)

def main():
  l = nodelexer.Lexer()
  l.build()
  p = Parser(l.tokens)
  p.build()

  while True:
    try:
      s = raw_input('> ')
      if s.strip() == 'quit()':
        break
    except EOFError:
      break
    if not s: continue
    p.parse(s)

if __name__ == '__main__':
  main()
