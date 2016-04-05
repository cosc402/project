import fulllexer
import viserror
import symbol
import ply.yacc as yacc
import sys

class Parser(object):
  def __init__(self, toklist):
    self.headsym = symbol.Env()
    self.cursym = None
    self.tokens = toklist

  #########################
  # GRAMMAR SPECIFICATION #
  #########################

  ##
  ## START SYMBOL
  ##

  def p_translation_unit(self, p):
    "translation_unit : declaration_seq"
    print 'FILE PARSED SUCCESSFULLY'

  # Empty production rule (eps)
  def p_eps(self, p):
    "eps :"
    print 'invoked epsilon (eps)'

  ##
  ## DECLARATIONS
  ##

  ### dcl.dcl ###

  def p_declaration_seq(self, p):
    """declaration_seq : declaration
                       | declaration_seq declaration"""
    print 'reduced to declaration_seq'

  def p_declaration(self, p):
    """declaration : block_declaration 
                   | function_definition 
                   | empty_declaration"""
    print 'reduced to declaration'

  def p_block_declaration(self, p):
    """block_declaration : simple_declaration"""
    print 'reduced to block_declaration'

  def p_simple_declaration(self, p):
    """simple_declaration : decl_specifier_seq init_declarator_list ';'
                          | decl_specifier_seq ';'
                          | init_declarator_list ';'
                          | ';'"""
    print 'reduced to simple_declaration'

  def p_empty_declaration(self, p):
    """empty_declaration : ';'"""
    print 'reduced to empty_declaration'

  ### dcl.spec ###

  def p_decl_specifier(self, p):
    """decl_specifier : type_specifier"""
    print 'reduced to decl_specifier'

  def p_decl_specifier_seq(self, p):
    """decl_specifier_seq : decl_specifier
                          | decl_specifier decl_specifier_seq"""
    print 'reduced to decl_specifier_seq'

  ### dcl.type ###

  def p_type_specifier(self, p):
    """type_specifier : trailing_type_specifier 
                      | class_specifier"""
    print 'reduced to type_specifier'

  def p_trailing_type_specifier(self, p):
    """trailing_type_specifier : simple_type_specifier
                               | elaborated_type_specifier
                               | cv_qualifier_seq"""
    print 'reduced to trailing_type_specifier'

  def p_type_specifier_seq(self, p):
    """type_specifier_seq : type_specifier 
                          | type_specifier type_specifier_seq"""
    print 'reduced to type_specifier_seq'

  ### dcl.type.simple ###

  def p_simple_type_specifier(self, p):
    """simple_type_specifier : SRES nested_name_specifier type_name
                             | nested_name_specifier type_name
                             | SRES type_name
                             | type_name
                             | CHAR 
                             | BOOL 
                             | SHORT 
                             | INT
                             | LONG 
                             | FLOAT 
                             | DOUBLE 
                             | VOID"""
    print 'reduced to simple_type_specifier'

  def p_type_name(self, p):
    """type_name : class_name"""
    print 'reduced to type_name'

  ### dcl.type.elab ###

  def p_elaborated_type_specifier(self, p):
    """elaborated_type_specifier : class_key SRES nested_name_specifier ID
                                 | class_key SRES ID
                                 | class_key nested_name_specifier ID
                                 | class_key ID"""
    print 'reduced to elaborated_type_specifier'

  ### dcl.decl ###

  def p_init_declarator_list(self, p):
    """init_declarator_list : init_declarator
                            | init_declarator_list ',' init_declarator"""
    print 'reduced to init_declarator_list'

  def p_init_declarator(self, p):
    """init_declarator : declarator 
                       | declarator initializer"""
    print 'reduced to init_declarator'

  def p_declarator(self, p):
    """declarator : noptr_declarator parameters_and_qualifiers"""
    print 'reduced to declarator'

  def p_noptr_declarator(self, p):
    """noptr_declarator : declarator_id
                        | noptr_declarator parameters_and_qualifiers
                        | noptr_declarator '[' constant_expression ']'
                        | noptr_declarator '[' ']'
                        | '(' noptr_declarator ')'"""
    print 'reduced to noptr_declarator'

  def p_parameters_and_qualifiers(self, p):
    """parameters_and_qualifiers : '(' parameter_declaration_clause ')' cv_qualifier_seq ref_qualifier"""
    print 'reduced to parameters_and_qualifiers'

  def p_cv_qualifier_seq(self, p):
    """cv_qualifier_seq : CONST"""
    print 'reduced to cv_qualifier_seq'

  def p_ref_qualifier(self, p):
    """ref_qualifier : '&'"""
    print 'reduced to ref_qualifier'

  def p_declarator_id(self, p):
    """declarator_id : id_expression
                     | SRES nested_name_specifier class_name
                     | SRES class_name
                     | nested_name_specifier class_name
                     | class_name"""
    print 'reduced to declarator_id'

  ### dcl.name ###

  def p_type_id(self, p):
    """type_id : type_specifier_seq 
               | type_specifier_seq abstract_declarator"""
    print 'reduced to type_id'

  def p_abstract_declarator(self, p):
    """abstract_declarator : noptr_abstract_declarator parameters_and_qualifiers
                           | parameters_and_qualifiers"""
    print 'reduced to abstract_declarator'

  def p_noptr_abstract_declarator(self, p):
    """noptr_abstract_declarator : noptr_abstract_declarator parameters_and_qualifiers
                                 | parameters_and_qualifiers
                                 | '(' noptr_abstract_declarator ')'
                                 | noptr_abstract_declarator '[' constant_expression ']'
                                 | '[' constant_expression ']'"""
    print 'reduced to noptr_abstract_declarator'

  ### dcl.fct ###

  def p_parameter_declaration_clause(self, p):
    """parameter_declaration_clause : parameter_declaration_list 
                                    | eps"""
    print 'reduced to parameter_declaration_clause'

  def p_parameter_declaration_list(self, p):
    """parameter_declaration_list : parameter_declaration
                                  | parameter_declaration_list ',' parameter_declaration"""
    print 'reduced to parameter_declaration_list'

  def p_parameter_declaration(self, p):
    """parameter_declaration : decl_specifier_seq declarator
                             | decl_specifier_seq declarator '=' initializer_clause
                             | decl_specifier_seq abstract_declarator
                             | decl_specifier_seq
                             | decl_specifier_seq abstract_declarator '=' initializer_clause
                             | decl_specifier_seq '=' initializer_clause"""
    print 'reduced to parameter_declaration'

  ### dcl.fct.def.general ###

  def p_function_definition(self, p):
    """function_definition : decl_specifier_seq declarator function_body
                           | declarator function_body"""
    print 'reduced to function_definition'

  def p_function_body(self, p):
    """function_body : ctor_initializer compound_statement 
                     | compound_statement"""
    print 'reduced to function_body'

  ### dcl.init ###

  def p_initializer(self, p):
    """initializer : brace_or_equal_initializer 
                   | '(' expression_list ')'"""
    print 'reduced to initializer'

  def p_brace_or_equal_initializer(self, p):
    """brace_or_equal_initializer : '=' initializer_clause"""
    print 'reduced to brace_or_equal_initializer'

  def p_initializer_clause(self, p):
    """initializer_clause : assignment_expression 
                          | braced_init_list"""
    print 'reduced to initializer_clause'

  def p_initializer_list(self, p):
    """initializer_list : initializer_clause
                        | initializer_list ',' initializer_clause"""
    print 'reduced to initializer_list'

  def p_braced_init_list(self, p):
    """braced_init_list : '{' initializer_list ',' '}'
                        | '{' initializer_list '}'
                        | '{' '}'"""
    print 'reduced to braced_init_list'

  ##
  ## STATEMENTS
  ##

  ### stmt.stmt ###

  def p_statement(self, p):
    """statement : labeled_statement
                 | expression_statement
                 | compound_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
                 | declaration_statement"""
    print 'reduced to statement'

  ### stmt.label ###

  def p_labeled_statement(self, p):
    """labeled_statement : CASE constant_expression ':' statement
                         | DEFAULT ':' statement"""
    print 'reduced to labeled_statement'

  ### stmt.expr ###

  def p_expression_statement(self, p):
    """expression_statement : expression ';' 
                            | ';'"""
    print 'reduced to expression_statment'

  ### stmt.block ###

  def p_compound_statment(self, p):
    """compound_statement : '{' statement_seq '}' 
                          | '{' '}'"""
    print 'reduced to compound_statement'

  def p_statement_seq(self, p):
    """statement_seq : statement 
                     | statement_seq statement"""
    print 'reduced to statement_seq'

  ### stmt.select ###

  def p_selection_statement(self, p):
    """selection_statement : IF '(' condition ')' statement
                           | IF '(' condition ')' statement ELSE statement
                           | SWITCH '(' condition ')' statement"""
    print 'reduced to selection_statement'

  def p_condition(self, p):
    """condition : expression
                 | decl_specifier_seq declarator '=' initializer_clause"""
    print 'reduced to condition'

  ### stmt.iter ###

  def p_iteration_statement(self, p):
    """iteration_statement : WHILE '(' condition ')' statement
                           | DO statement WHILE '(' expression ')' ';'
                           | FOR '(' for_init_statement condition ';' expression ')' statement
                           | FOR '(' for_init_statement ';' expression ')' statement
                           | FOR '(' for_init_statement condition ';' ')' statement
                           | FOR '(' for_init_statement ';' ')' statement"""
    print 'reduced to iteration_statement'

  def p_for_init_statement(self, p):
    """for_init_statement : expression_statement 
                          | simple_declaration"""
    print 'reduced to for_init_statement'

  ### stmt.jump ###

  def p_jump_statement(self, p):
    """jump_statement : BREAK ';'
                      | CONTINUE ';'
                      | RETURN expression ';'
                      | RETURN ';'"""
    print 'reduced to jump_statement'

  ### stmt.dcl ###

  def p_declaration_statement(self, p):
    """declaration_statement : block_declaration"""
    print 'reduced to declaration_statement'

  ##
  ## EXPRESSIONS
  ##

  ### expr.comma ###

  def p_expression(self, p):
    """expression : assignment_expression
                  | expression ',' assignment_expression"""
    print 'reduced to expression'

  ### expr.ass ###

  def p_assignment_expression(self, p):
    """assignment_expression : conditional_expression
                             | logical_or_expression assignment_operator initializer_clause"""
    print 'reduced to assignment_expression'

  def p_assignment_operator(self, p):
    """assignment_operator : EQ 
                           | MULEQ 
                           | DIVEQ 
                           | MODEQ 
                           | ADDEQ 
                           | SUBEQ"""
    print 'reduced to assignment_operator'

  ### expr.const ###

  def p_constant_expression(self, p):
    """constant_expression : conditional_expression"""
    print 'reduced to constant_expression'

  ### expr.cond ###

  def p_conditional_expression(self, p):
    """conditional_expression : logical_or_expression
                              | logical_or_expression '?' expression ':' assignment_expression"""
    print 'reduced to conditional_expression'

  ### expr.log.or ###

  def p_logical_or_expression(self, p):
    """logical_or_expression : logical_and_expression
                             | logical_or_expression LOR logical_and_expression"""
    print 'reduced to logical_or_expression'

  ### expr.log.and ###

  def p_logical_and_expression(self, p):
    """logical_and_expression : inclusive_or_expression
                              | logical_and_expression LAND inclusive_or_expression"""
    print 'reduced to logical_and_expression'

  ### expr.or ###

  def p_inclusive_or_expression(self, p):
    """inclusive_or_expression : exclusive_or_expression
                               | inclusive_or_expression '|' exclusive_or_expression"""
    print 'reduced to inclusive_or_expression'

  ### expr.xor ###

  def p_exclusive_or_expression(self, p):
    """exclusive_or_expression : and_expression
                               | exclusive_or_expression '^' and_expression"""
    print 'reduced to exclusive_or_expression'

  ### expr.bit.and ###

  def p_and_expression(self, p):
    """and_expression : equality_expression
                      | and_expression '&' equality_expression"""
    print 'reduced to and_expression'

  ### expr.eq ###

  def p_equality_expression(self, p):
    """equality_expression : relational_expression
                           | equality_expression EQ relational_expression
                           | equality_expression NEQ relational_expression"""
    print 'reduced to equality_expression'

  ### expr.rel ###

  def p_relational_expression(self, p):
    """relational_expression : shift_expression
                             | relational_expression '<' shift_expression
                             | relational_expression '>' shift_expression
                             | relational_expression LEQ shift_expression
                             | relational_expression GEQ shift_expression"""
    print 'reduced to relational_expression'

  ### expr.shift ###

  def p_shift_expression(self, p):
    """shift_expression : additive_expression
                        | shift_expression LSHIFT additive_expression
                        | shift_expression RSHIFT additive_expression"""
    print 'reduced to shift_expression'

  ### expr.add ###

  def p_additive_expression(self, p):
    """additive_expression : multiplicative_expression
                           | additive_expression '+' multiplicative_expression
                           | additive_expression '-' multiplicative_expression"""
    print 'reduced to additive_expression'

  ### expr.mul ###

  def p_multiplicative_expression(self, p):
    """multiplicative_expression : cast_expression
                                 | multiplicative_expression '*' cast_expression
                                 | multiplicative_expression '/' cast_expression
                                 | multiplicative_expression '%' cast_expression"""
    print 'reduced to multiplicative_expression'

  ### expr.cast ###

  def p_cast_expression(self, p):
    """cast_expression : unary_expression 
                       | '(' type_id ')' cast_expression"""
    print 'reduced to cast_expression'

  ### expr.unary ###

  def p_unary_expression(self, p):
    """unary_expression : postfix_expression
                        | INC cast_expression
                        | DEC cast_expression
                        | unary_operator cast_expression"""
    print 'reduced to unary_expression'

  def p_unary_operator(self, p):
    """unary_operator : '-' 
                      | '!' 
                      | '~'"""
    print 'reduced to unary_operator'

  ### expr.post ###

  def p_postfix_expression(self, p):
    """postfix_expression : primary_expression
                          | postfix_expression '[' expression ']'
                          | postfix_expression '(' expression_list ')'
                          | postfix_expression '(' ')'
                          | simple_type_specifier '(' expression_list ')'
                          | simple_type_specifier '(' ')'
                          | postfix_expression '.' id_expression
                          | postfix_expression INC
                          | postfix_expression DEC
                          | SCAST '<' type_id '>' '(' expression ')'"""
    print 'reduced to postfix_expression'

  def p_expression_list(self, p):
    """expression_list : initializer_list"""
    print 'reduced to expression_list'

  ### expr.prim.general ###

  def p_primary_expression(self, p):
    """primary_expression : literal
                          | THIS
                          | '(' expression ')'
                          | id_expression"""
    print 'reduced to primary_expression'

  def p_id_expression(self, p):
    """id_expression : unqualified_id 
                     | qualified_id"""
    print 'reduced to id_expression'

  def p_unqualified_id(self, p):
    """unqualified_id : ID 
                      | '~' class_name 
                      | template_id"""
    print 'reduced to unqualified_id'

  def p_qualified_id(self, p):
    """qualified_id : SRES nested_name_specifier unqualified_id
                    | nested_name_specifier unqualified_id
                    | SRES ID
                    | SRES template_id"""
    print 'reduced to qualified_id'

  def p_nested_name_specifier(self, p):
    """nested_name_specifier : type_name SRES
                             | nested_name_specifier ID SRES
                             | nested_name_specifier simple_template_id SRES"""
    print 'reduced to nested_name_specifier'

  ##
  ## CLASSES
  ##

  ### class ###

  def p_class_name(self, p):
    """class_name : ID"""
    print 'reduced to class_name'

  def p_class_specifier(self, p):
    """class_specifier : class_head '{' member_specification '}' 
                       | class_head '{' '}'"""
    print 'reduced to class_specifier'

  def p_class_head(self, p):
    """class_head : class_key class_head_name 
                  | class_key"""
    print 'reduced to class_head'

  def p_class_head_name(self, p):
    """class_head_name : nested_name_specifier class_name 
                       | class_name"""
    print 'reduced to class_head_name'

  def p_class_key(self, p):
    """class_key : CLASS 
                 | STRUCT"""
    print 'reduced to class_key'

  ### class.mem ###

  def p_member_specification(self, p):
    """member_specification : member_declaration member_specification
                            | member_declaration
                            | access_specifier ':' member_specification
                            | access_specifier ':'"""
    print 'reduced to member_specification'

  def p_member_declaration(self, p):
    """member_declaration : decl_specifier_seq member_declarator_list ';'
                          | member_declarator_list ';'
                          | decl_specifier_seq ';'
                          | ';'
                          | function_definition ';'
                          | function_definition"""
    print 'reduced to member_declaration'

  def p_member_declarator_list(self, p):
    """member_declarator_list : member_declarator 
                              | member_declarator_list ',' member_declarator"""
    print 'reduced to member_declarator_list'

  def p_member_declarator(self, p):
    """member_declarator : declarator brace_or_equal_initializer 
                         | declarator"""
    print 'reduced to member_declarator'

  ### class.derived ###

  def p_class_or_decltype(self, p):
    """class_or_decltype : SRES nested_name_specifier class_name
                         | SRES class_name
                         | nested_name_specifier class_name
                         | class_name"""
    print 'reduced to class_or_decltype'

  def p_access_specifier(self, p):
    """access_specifier : PRIVATE 
                        | PUBLIC"""
    print 'reduced to access_specifier'

  ### class.base.init ###

  def p_ctor_initializer(self, p):
    """ctor_initializer : ':' mem_initializer_list"""
    print 'reduced to ctor_initializer'

  def p_mem_initializer_list(self, p):
    """mem_initializer_list : mem_initializer 
                            | mem_initializer ',' mem_initializer_list"""
    print 'reduced to mem_initializer_list'

  def p_mem_initializer(self, p):
    """mem_initializer : mem_initializer_id '(' expression_list ')' 
                       | mem_initializer_id '(' ')'"""
    print 'reduced to mem_initializer'

  def p_mem_initializer_id(self, p):
    """mem_initializer_id : class_or_decltype 
                          | ID"""
    print 'reduced to mem_initializer_id'

  ##
  ## TEMPLATES
  ##

  ### temp.names ###

  def p_simple_template_id(self, p):
    """simple_template_id : template_name '<' template_argument_list '>' 
                          | template_name '<' '>'"""
    print 'reduced to simple_template_id'

  def p_template_id(self, p):
    """template_id : simple_template_id"""
    print 'reduced to template_id'

  def p_template_name(self, p):
    """template_name : ID"""
    print 'reduced to template_name'

  def p_template_argument_list(self, p):
    """template_argument_list : template_argument 
                              | template_argument_list ',' template_argument"""
    print 'reduced to template_argument_list'

  def p_template_argument(self, p):
    """template_argument : constant_expression 
                         | type_id 
                         | id_expression"""
    print 'reduced to template_argument'

  ##
  ## LEXICAL
  ##

  ### lex.literal.kinds ###

  def p_literal(self, p):
    """literal : ICON
               | CCON
               | FCON
               | SCON
               | TRUE
               | FALSE"""
    print 'reduced to literal'

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

  lexer = fulllexer.Lexer()
  lexer.build()
  parser = Parser(lexer.tokens)
  parser.build()

  fin = open(sys.argv[1])
  parser.parse(fin.read())
