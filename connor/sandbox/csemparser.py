import csemlexer
import viserror
import symbol
import ply.yacc as yacc
import sys

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

  def p_externs(self, p):
    """externs :
               | externs extern"""
    print 'reduced to externs'

  def p_extern(self, p):
    """extern : dcl ';'
              | func"""
    print 'reduced to extern'

  def p_dcls(self, p):
    """dcls : 
            | dcls dcl ';'"""
    print 'reduced to dcls'

  def p_dcl(self, p):
    """dcl : type dclr
           | dcl ',' dclr"""
    print 'reduced to dcl'

  def p_dclr(self, p):
    """dclr : ID
            | ID '[' ']'
            | ID '[' ICON ']'"""
    print 'reduced to dclr'

  def p_type(self, p):
    """type : CHAR
            | FLOAT
            | DOUBLE
            | INT"""
    print 'reduced to type'

  def p_func(self, p):
    """func : fhead stmts '}'"""
    print 'reduced to func'

  def p_fhead(self, p):
    """fhead : fname fargs '{' dcls"""
    print 'reduced to fhead'

  def p_fname(self, p):
    """fname : type ID
             | ID"""
    print 'reduced to fname'

  def p_fargs(self, p):
    """fargs : '(' ')'
             | '(' args ')'"""
    print 'reduced to fargs'

  def p_args(self, p):
    """args : type dclr
            | args ',' type dclr"""
    print 'reduced to args'

  def p_block(self, p):
    """block : '{' stmts '}'"""
    print 'reduced to block'

  def p_stmts(self, p):
    """stmts :
             | stmts stmt"""
    print 'reduced to stmts'

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