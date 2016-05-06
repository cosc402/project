import csemlexer
import viserror
import symbol
import ply.yacc as yacc
import sys
from syntax import *

# global
DEBUG = False

class Parser(object):
  def __init__(self, toklist):
    self.headsym = symbol.Env()
    self.cursym = None
    self.tokens = toklist
    self.ast = None         # this member is set to the root of the AST after parsing

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
    p[0] = Node('prog', p[1])
    self.ast = SyntaxTree(p[0])
    if DEBUG: print 'reduced to {}. Parsing completed successfully!'.format(p[0])

  def p_externs(self, p):
    """externs :
               | externs extern"""
    p[0] = Node('externs', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_extern(self, p):
    """extern : dcl ';'
              | func"""
    p[0] = Node('extern', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_dcls(self, p):
    """dcls : 
            | dcls dcl ';'"""
    p[0] = Node('dcls', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_dcl(self, p):
    """dcl : type dclr
           | dcl ',' dclr"""
    p[0] = Node('dcl', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_dclr(self, p):
    """dclr : ID
            | ID '[' ']'
            | ID '[' ICON ']'"""
    p[0] = Node('dclr', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_type(self, p):
    """type : CHAR
            | FLOAT
            | DOUBLE
            | INT"""
    p[0] = Node('type', p[1])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_func(self, p):
    """func : fhead stmts '}'"""
    p[0] = Node('func', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_fhead(self, p):
    """fhead : fname fargs '{' dcls"""
    p[0] = Node('fhead', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_fname(self, p):
    """fname : type ID
             | ID"""
    p[0] = Node('fname', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_fargs(self, p):
    """fargs : '(' ')'
             | '(' args ')'"""
    p[0] = Node('fargs', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_args(self, p):
    """args : type dclr
            | args ',' type dclr"""
    p[0] = Node('args', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_block(self, p):
    """block : '{' stmts '}'"""
    p[0] = Node('block', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_stmts(self, p):
    """stmts :
             | stmts stmt"""
    p[0] = Node('stmts', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

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
    p[0] = Node('stmt', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_cexpro(self, p):
    """cexpro : 
              | cexpr"""
    p[0] = Node('cexpro', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

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
    p[0] = Node('cexpr', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_exprs(self, p):
    """exprs : expr
             | exprs ',' expr"""
    p[0] = Node('exprs', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_expro(self, p):
    """expro : 
             | expr"""
    p[0] = Node('expro', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

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
            | ID '(' ')'
            | ID '(' exprs ')'
            | '&' lval
            | '-' expr %prec UMINUS
            | lval %prec LVAL
            | '(' expr ')'
            | constant"""
    p[0] = Node('expr', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_lval(self, p):
    """lval : ID
            | ID '[' expr ']'"""
    p[0] = Node('lval', *p[1:])
    if DEBUG: print 'reduced to {}'.format(p[0])

  def p_constant(self, p):
    """constant : SCON
                | ICON
                | CCON
                | FCON"""
    p[0] = Node('constant', p[1])
    if DEBUG: print 'reduced to {}'.format(p[0])

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