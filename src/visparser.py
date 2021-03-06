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
    ('left','+','-', 'INCREMENT','DECREMENT'),
    ('left','*','/','%'),
    ('right','UMINUS')
  )

  # ASSIGNMENTS
  def p_statement_assign(self, p):
    'statement : ID "=" expression ";"'
    self.headsym.update(p[1], p[3])

  def p_statement_inc_assign(self, p):
    'statement : ID PLUSEQUAL expression ";"'
    self.headsym.update(p[1],self.headsym.get(p[1]).value + p[3])
  
  def p_statement_dec_assign(self, p):
    'statement : ID MINUSEQUAL expression ";"'
    self.headsym.update(p[1],self.headsym.get(p[1]).value - p[3])
  
  def p_statement_decl_assign(self, p):
    'statement : declaration ID "=" expression ";"'
    self.headsym.put(p[2], p[1], p[4])
  
  def p_statement_decl_assign_char(self, p):
    'statement : declaration ID "=" "\'" CHARACTER "\'" ";"'
    self.headsym.put(p[2], p[1], p[5])
  
  def p_statement_decl_assign_str(self, p):
    '''statement : declaration ID '=' '\"' ID '\"' ';' '''
    self.headsym.put(p[2], p[1], p[5])

  # STDOUT
  def p_statement_cout(self, p):
    'statement : COUT out ";"'
  
  def p_statement_decl(self, p):
    'statement : declaration ID ";"'
    self.headsym.put(p[2], p[1], None)
  
  #INCREMENT / DECREMENT
  def p_statemnt_inc(self, p):
    "statement : ID INCREMENT ';'"
    self.headsym.update(p[1],self.headsym.get(p[1]).value + 1)
  
  def p_statement_dec(self, p):
    "statement : ID DECREMENT ';'"
    self.headsym.update(p[1],self.headsym.get(p[1]).value - 1)
  
  # OUT STATEMENTS
  def p_out_rec(self, p):
    'out : out out'

  def p_out_literal(self, p):
    '''out : INSERT '\"' ID '\"' 
           | INSERT "\'" CHARACTER "\'" '''
    print(p[3])

  def p_out(self, p):
    'out : INSERT expression'
    print(p[2])

  # DECLARATIONS
  def p_decl_var(self, p):
    '''declaration : INT
                   | DOUBLE
                   | FLOAT
                   | CHAR
                   | BOOL
                   | STRING'''
    p[0] = p[1]

  # ARITHMATIC
  def p_expression_binop(self, p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression'''
    if p[2] == '+':    p[0] = p[1] + p[3]
    elif p[2] == '-':  p[0] = p[1] - p[3]
    elif p[2] == '*':  p[0] = p[1] * p[3]
    elif p[2] == '/':  p[0] = p[1] / p[3]
    elif p[2] == '%':  p[0] = p[1] % p[3]

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
