import csemlexer
import viserror
import symbol
import ply.yacc as yacc
import sys
from node import *

class Parser(object):
  def __init__(self, toklist):
    self.headsym = symbol.Env()
    self.cursym = None
    self.tokens = toklist

  precedence = (
    ('right', 'LVAL'),
    ('right','=','ADDEQ','SUBEQ','MULEQ','DIVEQ','MODEQ'),
    ('left','LOR'),
    ('left','LAND'),
    ('left','EQ','NEQ'),
    ('left','<','>','LEQ','GEQ'),
    ('left','LSHIFT','RSHIFT'),
    ('left','+','-'),
    ('left','*','/','%'),
    ('right','UMINUS','!')
  )

  #########################
  # GRAMMAR SPECIFICATION #
  #########################

  def p_prog(self, p):
    """prog : externs"""
    print 'reduced to prog. Parsing completed successfully!'
    p[0] = Node('prog', p[1])
    self.syntaxtree = SyntaxTree(p[0])

  def p_externs(self, p):
    """externs :
               | externs extern"""
    print 'reduced to externs'
    if len(p) == 1:
      p[0] = Node('externs')
    else: p[0] = Node('externs', 0, p[1], p[2])

  def p_extern(self, p):
    """extern : dcl ';'
              | func"""
    print 'reduced to extern'
    if len(p) == 3:
      p[0] = Node('extern', 0, p[1], ';')
    else: p[0] = Node('extern', 0, p[1])

  def p_dcls(self, p):
    """dcls : 
            | dcls dcl ';'"""
    print 'reduced to dcls'
    if len(p) == 1:
      p[0] = Node('dcls', 0)
    else: p[0] = Node('dcls', 0, p[1], p[2], ';')

  def p_dcl(self, p):
    """dcl : type dclr
           | dcl ',' dclr"""
    print 'reduced to dcl'
    if len(p) == 3:
      p[0] = Node('dcl', 0, p[1], p[2])
    else: p[0] = Node('dcl', 0, p[1], ',', p[3])

  def p_dclr(self, p):
    """dclr : ID
            | ID '[' ']'
            | ID '[' ICON ']'"""
    print 'reduced to dclr'
    n = Node('ID', p[1])
    if len(p) == 2:
      p[0] = Node('dclr', 0, n)
    elif len(p) == 4:
      p[0] = Node('dclr', 0, n, '[', ']')
    else: 
      m = Node('ICON', p[3])
      p[0] = Node('dclr', 0, n, '[', m, ']')

  def p_type(self, p):
    """type : CHAR
            | FLOAT
            | DOUBLE
            | INT"""
    print 'reduced to type'
    n = Node(csemlexer.Lexer.reserved[p[1]], p[1])
    p[0] = Node('type', 0, n)

  def p_func(self, p):
    """func : fhead stmts '}'"""
    print 'reduced to func'
    p[0] = Node('func', 0, p[1], p[2])

  def p_fhead(self, p):
    """fhead : fname fargs '{' dcls"""
    print 'reduced to fhead'
    p[0] = Node('fhead', 0, p[1], p[2], '{', p[4])

  def p_fname(self, p):
    """fname : type ID
             | ID"""
    print 'reduced to fname'
    if len(p) == 3:
      n = Node('ID', p[2])
      p[0] = Node('fname', 0, p[1], n)
    else:
      n = Node('ID', p[1])
      p[0] = Node('fname', 0, n)

  def p_fargs(self, p):
    """fargs : '(' ')'
             | '(' args ')'"""
    print 'reduced to fargs'
    if len(p) == 3:
      p[0] = Node('fargs', 0, '(', ')')
    else: p[0] = Node('fargs', 0, '(', p[2], ')')

  def p_args(self, p):
    """args : type dclr
            | args ',' type dclr"""
    print 'reduced to args'
    if len(p) == 3:
      p[0] = Node('args', 0, p[1], p[2])
    else: p[0] = Node('args', 0, p[1], ',', p[3], p[4])

  def p_block(self, p):
    """block : '{' stmts '}'"""
    print 'reduced to block'
    p[0] = Node('block', 0, '{', p[2], '}')

  def p_stmts(self, p):
    """stmts :
             | stmts stmt"""
    print 'reduced to stmts'
    if len(p) == 1:
      p[0] = Node('stmts', 0)
    else: p[0] = Node('stmts', 0, p[1], p[2])

  def p_stmt(self, p):
    """stmt : expr ';'
            | IF '(' cexpr ')' stmt
            | IF '(' cexpr ')' stmt ELSE stmt
            | WHILE '(' cexpr ')' stmt
            | DO stmt WHILE '(' cexpr ')' ';'
            | FOR '(' expro ';' cexpro ';' expro ')' stmt
            | CONTINUE ';'
            | BREAK ';'
            | RETURN ';'
            | RETURN expr ';'
            | block
            | ';'"""
    print 'reduced to stmt'
    if p[1] == ';':                     # empty statement
      p[0] = Node('stmt', 0, ';')
    elif len(p) == 2:                   # block
      p[0] = Node('stmt', 0, p[1])
    elif len(p) == 3:
      p[0] = Node('stmt', 0, p[1], ';')
    elif len(p) == 4:
      p[0] = Node('stmt', 0, p[1], p[2], ';')
    elif len(p) == 6:
      p[0] = Node('stmt', 0, p[1], '(', p[3], ')', p[5])
    elif len(p) == 8:
      if p[1].label == 'IF':
        p[0] = Node('stmt', 0, p[1], '(', p[3], ')', p[5], p[6], p[7])
      else:
        pass

  def p_cexpro(self, p):
    """cexpro : 
              | cexpr"""
    print 'reduced to cexpro'

  def p_cexpr(self, p):
    """cexpr : expr EQ expr
             | expr NEQ expr
             | expr LEQ expr
             | expr GEQ expr
             | expr '<' expr
             | expr '>' expr
             | cexpr LAND cexpr
             | cexpr LOR cexpr
             | '!' cexpr
             | expr"""
    print 'reduced to cexpr'

  def p_exprs(self, p):
    """exprs : expr
             | exprs ',' expr"""
    print 'reduced to exprs'

  def p_expro(self, p):
    """expro : 
             | expr"""
    print 'reduced to expro'

  def p_expr(self, p):
    """expr : lval '=' expr
            | lval ADDEQ expr
            | lval SUBEQ expr
            | lval MULEQ expr
            | lval DIVEQ expr
            | lval MODEQ expr
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr '%' expr
            | expr LSHIFT expr
            | expr RSHIFT expr
            | '&' lval
            | '-' expr %prec UMINUS
            | lval %prec LVAL
            | ID '(' ')'
            | ID '(' exprs ')'
            | '(' expr ')'
            | constant"""
    print 'reduced to expr'

  def p_lval(self, p):
    """lval : ID
            | ID '[' expr ']'"""
    print 'reduced to lval'

  def p_constant(self, p):
    """constant : SCON
                | ICON
                | CCON
                | FCON"""
    print 'reduced to constant'

  ################################
  # END OF GRAMMAR SPECIFICATION #
  ################################

  ###
  ### PARSER FUNCTIONS
  ###

  def p_error(self, p):
    if p:
      print "Syntax error at '{}'".format(p.value)
      print "Symbol type '{}'".format(p.type)
    else:
      print "Syntax error at EOF."

  def build(self, **kwargs):
    self.parser = yacc.yacc(module=self, **kwargs)

  def parse(self, data):
    self.parser.parse(data)

#################################################################

####################
#
# test procedure
#

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Please supply input source file.'
    exit()

  lexer = csemlexer.Lexer()
  lexer.build()
  parser = Parser(lexer.tokens)
  parser.build()

  fin = open(sys.argv[1])
  parser.parse(fin.read())