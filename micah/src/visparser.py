import vislexer
import viserror
import symbol
import ply.yacc as yacc

class Parser(object):
  def __init__(self, toklist):
    self.headsym = symbol.Env()
    self.cursym = None
    self.tokens = toklist

  precedence = (
    ('left','INSERT'), # and EXTRACT
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS')
  )

  def p_statement_assign(self, p):
    'statement : ID "=" expression ";"'
    self.headsym.update(p[1], p[3])

  def p_statement_decl_assign(self, p):
    'statement : declaration ID "=" expression ";"'
    self.headsym.put(p[2], p[1], p[4])

  def p_statement_cout(self, p):
    'statement : COUT INSERT expression ";"'
    print(p[3])

  def p_statement_decl(self, p):
    'statement : declaration ID ";"'
    self.headsym.put(p[2], p[1], None)

  def p_decl_var(self, p):
    '''declaration : INT
                   | DOUBLE
                   | FLOAT
                   | CHAR
                   | BOOL'''
    p[0] = p[1]

  def p_expression_binop(self, p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':    p[0] = p[1] + p[3]
    elif p[2] == '-':  p[0] = p[1] - p[3]
    elif p[2] == '*':  p[0] = p[1] * p[3]
    elif p[2] == '/':  p[0] = p[1] / p[3]

  def p_expression_uminus(self, p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

  def p_expression_group(self, p):
    "expression : '(' expression ')'"
    p[0] = p[2]

  def p_expression_number(self, p):
    "expression : NUM"
    p[0] = p[1]

  def p_expression_character(self, p):
    "expression : CHARACTER"
    p[0] = p[1]

  def p_expression_id(self, p):
    "expression : ID"
    p[0] = self.headsym.get(p[1]).value

  # end of grammar definition #

  def p_error(self, p):
    if p:
      print("Syntax error at '{}'".format(p.value))
      print("Symbol type '{}'".format(p.type))
    else:
      print("Syntax error at EOF")

  def build(self, **kwargs):
    self.parser = yacc.yacc(module=self, **kwargs)

  def parse(self, data):
    self.parser.parse(data)


#### Run this module to test ####

def main():
  lexer = vislexer.Lexer()
  lexer.build()
  parser = Parser(lexer.tokens)
  parser.build()

  while True:
    try:
      s = raw_input('test > ')
      if s == 'quit()':
        break
    except EOFError:
      break
    if not s: continue
    parser.parse(s)
    parser.headsym.print_table()

if __name__ == '__main__':
  main()