import symbol as sym
import viserror as err
import copy
from control import *

DEBUG = False

#
# Node(label, *children, **kwargs)
#
# A node in the parse tree. This represents a
# nonterminal in the syntax tree produced by PLY.
#
# USAGE
# 
#   You can treat a node object like a list of its children! For example, to
#   iterate through a node's children,
# 
#       node = Node('label', 'child1', 'child2')
#       for child in node:
#           print child
#
#   You can also access specific children:
# 
#       print node[1]       # (prints "child2")
#
#   You can get the number of children by calling len():
#
#       print 'This node has', len(node), 'children.'
#
# MEMBERS
#   
#   label : a string matching the name of the grammar symbol corresponding to
#     this node in the syntax tree.
#
#   parent : If this node has a parent in the syntax tree, this member is a
#     pointer to the parent node.
#
#   children : usually Node objects that represent this node's children in the
#     syntax tree. When the children are passed through the constructor,
#     the constructor connects each children's parent member.
#
#   value : You can use this variable to store anything that would be
#     useful to remember in traversing the syntax tree.
#
#   symtab : an instance of Env that represents a sort of
#     "prototype" symbol table for this node. In the first pass
#     through the syntax tree, the interpreter will find the
#     un-nested variable declarations in this node's subtree and 
#     put those variables into symtab.
#   
# METHODS
#
#   __str__() : Get a string of the node's label, value, and labels of 
#     immediate children.
#
#   __iter__() : This allows you to iterate through the children of the node.
#     (e.g., for child in node: ...)
#
class Node:
  def __init__(self, label, *children, **kwargs):
    self.parent = None
    self.symtab = None 
    self.label = label
    self.value = kwargs.get('value', None)

    for child in children:
      if isinstance(child, Node):
        child.parent = self
    self.children = children

  def __str__(self):
    s = 'Node({}'.format(self.label)
    if self.value != None:
      s += '({})'.format(self.value)
    if len(self.children) == 0:
      return s + ')'
    for child in self.children:
      if isinstance(child, Node):
        s += ', {}'.format(child.label)
        if child.value != None:
          s += '({})'.format(child.value)
      else: s += ', ' + str(child)
    return s + ')'

  def __iter__(self):
    return iter(self.children)

  def __len__(self):
    return len(self.children)

  def __getitem__(self, index):
    return self.children[index]

  # attach a symbol table to this node
  def initSymbolTable(self, symtab=None):
    if symtab == None:
      self.symtab = sym.Env()
    else:
      self.symtab = symtab

  # insert an identifier-entry pair into the existing symbol table
  # associated with the closest ancestor of this node. The 'entry' is
  # a pre-constructed object of a subclass of Symbol. The subclass should 
  # be chosen with regard to the type of the symbol (int, function, float...).
  def put(self, id, obj):
    if self.symtab == None:
      if self.parent == None:
        raise err.VisError('No symbol table exists to put "{}".'.format(name))
      else:
        self.parent.put(id, obj)
    else:
      self.symtab.put(id, obj)

  # retrieve the value of the entry in the symbol table
  # associated with the closest ancestor of this node
  def get(self, id):
    if self.symtab == None:
      if self.parent == None:
        raise err.VisError('"{}" does not exist in any symbol table.'.format(name))
      else:
        return self.parent.get(id)
    else:
      return self.symtab.get(id)

  # dump all symbol tables accessible by the current scope
  def printTable(self):
    level = 0
    nd = self
    print 'Identifier Space:'
    print '=============================================='
    print 'Innermost Scope'
    print '-----------------------------------------'
    while nd != None:
      if nd.symtab == None:
        nd = nd.parent
        continue
      if level > 0:
        print '=========================================='
        print 'Scope +{}'.format(level)
        print '------------------------------------------'
      for sym in nd.symtab.table.values():
        print '  ', sym
      level += 1
      nd = nd.parent
    print '=============================================='

###############################################################

#
# checkNode(nd)
#
# Check whether nd is an instance of Node and throw an error if not.
#
def checkNode(nd, func='<function name>'):
  if not isinstance(nd, Node):
    raise err.VisError('Must use Node in {}. Used {}'.format(func, type(nd)))

#
# SyntaxTree
#
# Structure that should contain the AST after the parser returns.
# Defines traversal operations.
#
class SyntaxTree:
  def __init__(self, root=None):
    self.root = root      # root node holds the global symbol table
    self.cur = root
    self.main = None      # pointer to the main() subtree with root `func'
    self.stop = True      # controls where the step() function returns
    self.callstack = []   # stack containing recovery pointers to function nodes saved during execution
    self.symstack = []    # stack containing malleable symbol tables during execution

    #
    # Dictionary of first-pass rules for nodes. Keyed on a string that should match
    # the label of the node for which the rule is written.
    #
    self.init_ = {
      'prog':             self.init_prog,
      'externs':          self.init_externs,
      'extern':           self.init_extern,
      'dcls':             self.init_dcls,
      'dcl':              self.init_dcl,
      'dclr':             self.init_dclr,
      'type':             self.init_type,
      'func':             self.init_func,
      'fhead':            self.init_fhead,
      'fname':            self.init_fname,
      'fargs':            self.init_fargs,
      'args':             self.init_args,
      'block':            self.init_block,
      'stmts':            self.init_stmts,
      'stmt':             self.init_stmt,
      'cexpro':           self.init_cexpro,
      'cexpr':            self.init_cexpr,
      'exprs':            self.init_exprs,
      'expro':            self.init_expro,
      'expr':             self.init_expr,
      'lval':             self.init_lval,
      'constant':         self.init_constant
    }

    #
    # Dictionary of second-pass rules for nodes. Keyed on a string that should match
    # the label of the node for which the rule is written.
    #
    self.exec_ = {
      'prog':             self.exec_prog,
      'externs':          self.exec_externs,
      'extern':           self.exec_extern,
      'dcls':             self.exec_dcls,
      'dcl':              self.exec_dcl,
      'dclr':             self.exec_dclr,
      'type':             self.exec_type,
      'func':             self.exec_func,
      'fhead':            self.exec_fhead,
      'fname':            self.exec_fname,
      'fargs':            self.exec_fargs,
      'args':             self.exec_args,
      'block':            self.exec_block,
      'stmts':            self.exec_stmts,
      'stmt':             self.exec_stmt,
      'cexpro':           self.exec_cexpro,
      'cexpr':            self.exec_cexpr,
      'exprs':            self.exec_exprs,
      'expro':            self.exec_expro,
      'expr':             self.exec_expr,
      'lval':             self.exec_lval,
      'constant':         self.exec_constant
    }

  def dump(self):
    level = 1
    print 'Identifier Space:'
    print '=============================================='
    print 'Innermost Scope'
    print '-----------------------------------------'
    while level <= len(self.symstack):
      symtab = self.symstack[-level]
      if level > 1:
        print '=========================================='
        print 'Scope +{}'.format(level-1)
        print '------------------------------------------'
      for sym in symtab.table.values():
        print '  ', sym
      level += 1
    print '=============================================='

  #
  # getSymbol(id)
  #
  # Get the topmost instance of the symbol (in the stack) associated with
  # the string identifier `id'. If no such symbol exists, returns None.
  #
  def getSymbol(self, id):
    i = len(self.symstack) - 1
    while i >= 0:
      symtab = self.symstack[i]
      symbol = symtab.get(id)
      if symbol != None:
        return symbol
      else: i -= 1
    return None

  #
  # putSymbol(id, symbol, force=False)
  #
  # Put a new symbol into the symbol table stack. If you want to update a symbol,
  # use getSymbol() and call .update() on the symbol instead. Returns true if successful.
  # Otherwise, returns False.
  #
  def putSymbol(self, id, symbol, force=False):
    if len(self.symstack) == 0:
      return False
    self.symstack[-1].put(id, symbol, force)
    return True

  #
  # pushScope(symtab=None)
  #
  # Push a COPY of the symbol table `symtab' onto the stack. If no symbol table is
  # passed as an argument, an empty symbol table is pushed onto the stack.
  #
  def pushScope(self, symtab=None):
    if symtab == None:
      new_symtab = sym.Env()
    else: new_symtab = copy.deepcopy(symtab)      # XXX This looks dangerous...
    self.symstack.append(new_symtab)

  #
  # popScope()
  #
  # Pop a symbol table from the stack. Returns True if the operation was successful
  # and False otherwise.
  #
  def popScope(self):
    if len(self.symstack) == 0:
      return False
    self.symstack.pop()
    return True

  #
  # topScope()
  #
  # Get the top symbol table Env from the stack. If the stack is empty, returns None.
  #
  def topScope(self):
    if len(self.symstack) == 0:
      return None
    return symstack[-1]

  #
  # pushBreakpoint(breakpoint)
  #
  # Push the Breakpoint onto the stack of return addresses. The idea is to
  # store a point of return when there might be an abrubt change in control
  # flow somewhere in the subtree. A breakpoint could be a function node or
  # iteration statement node.
  #
  def pushBreakpoint(self, breakpoint):
    self.callstack.append(breakpoint)

  #
  # popBreakpoint(type=None)
  #
  # Pop a Breakpoint from the callstack. If `type' is specified, continue popping
  # Breakpoints until a Breakpoint with the specified type is on top of the stack.
  # Returns False if the operation failed for any reason. Returns True otherwise.
  #
  def popBreakpoint(self, type=None):
    if len(self.callstack) == 0:
      return False

    # type not given: pop one breakpoint
    if type == None:
      self.callstack.pop()
      return True

    # type given: pop until type of breakpoint remains on top
    while len(self.callstack) > 0 and self.callstack[-1].type != type:
      self.callstack.pop()
    if len(self.callstack) > 0: return True
    else: return False

  #
  # topBreakpoint()
  #
  # Peek at the top Breakpoint in the callstack. If none exists, returns None.
  #
  def topBreakpoint(self):
    return self.callstack[-1]

  def printTree(self, nd=None, level=0):
    if nd == None:
      nd = self.root
    if not isinstance(nd, Node):
      print '{}leaf {}'.format(' '*level, nd)
      return 
    print '{}node {}'.format(' '*level, nd.label)
    for child in nd:
      self.printTree(child, level+2)

  # Wrapper for calling the first-pass rules.
  # Initialize the subtree with root `nd'.
  def descend(self, nd=None):
    if nd == None: nd = self.cur
    return self.init_[nd.label](nd)

  # Wrapper for calling the second-pass rules.
  # Execute or evaluate the subtree with root `nd'.
  def execute(self, nd=None):
    if nd == None: nd = self.root
    return self.exec_[nd.label](nd)

  # initialize the symbol tables
  def init(self):
    self.descend(self.root)

  #########################
  # 
  # FIRST PASS SYMBOL TABLE INITIALIZER FUNCTIONS
  #
  # Each of these functions takes an AST node as a parameter
  # and each may return a result (return `None' if no value
  # should be returned). The function `init_XXX' descends into
  # the subtree whose root is the node `nd', where nd.label
  # must be 'XXX'. If the label does not match, bad things
  # surely await you.
  #
  # The result of all of these functions is to initialize prototype symbol
  # tables and attach them to the nodes that represent scopes.
  # Once this pass has been made, the interpreter is ready to
  # execute the program using the rules defined in the
  # `exec_XXX()' functions.
  #
  # Any function that returns anything useful should also set
  # that node's `init_value' to whatever is returned.
  #

  def init_prog(self, nd):
    checkNode(nd, 'init_prog')
    # prog --> externs
    # This is the start symbol. This node will house the
    # global symbol table.
    nd.initSymbolTable()
    self.descend(nd[0])
    if DEBUG: print 'initial descent complete'

  def init_externs(self, nd):
    checkNode(nd, 'init_externs')
    # externs --> 
    #           | externs extern
    for child in nd:
      self.descend(child)

  def init_extern(self, nd):
    checkNode(nd, 'init_extern')
    # extern --> dcl ';'
    #          | func
    for child in nd:
      if isinstance(child, Node):
        self.descend(child)

  def init_dcls(self, nd):
    checkNode(nd, 'init_dcls')
    # dcls -->
    #        | dcls dcl ';'
    for child in nd:
      if isinstance(child, Node):
        self.descend(child)

  def init_dcl(self, nd):
    '''Returns a XXXSymbol object to carry the type across a
    comma-separated list of declarations.'''
    checkNode(nd, 'init_dcl')

    # dcl --> type dclr
    # `type' nodes return a XXXSymbol after evaluation. Use
    # this as a constructor and then add to the symbol table.
    if len(nd) == 2:
      typ = self.descend(nd[0])      # XXXSymbol
      dclr = self.descend(nd[1])     # 1- or 2-tuple
      identifier = dclr[0]
      if len(dclr) == 1:
        nd.put(identifier, typ(identifier))
      else:
        nd.put(identifier, sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1]))
      nd.init_value = typ
      return typ

    # dcl --> dcl ',' dclr
    # The type that should be carried over into the other dclr is obtained
    # from descending the `dcl' child.
    typ = self.descend(nd[0])
    dclr = self.descend(nd[2])
    identifier = dclr[0]
    if len(dclr) == 1:
      nd.put(identifier, typ(identifier))
    else:
      nd.put(identifier, sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1]))
    nd.init_value = typ
    return typ

  def init_dclr(self, nd):
    '''Returns either a 1- or 2-tuple, depending on the derivation:
    If dclr --> ID
      return ("identifier",)
    If dclr --> ID '[' ']'        // second element None indicates array of unknown size
      return ("identifier", None)
    If dclr --> ID '[' ICON ']'
      return ("identifier", size of array)'''
    checkNode(nd, 'init_dclr')

    # dclr --> ID
    if len(nd) == 1:
      nd.init_value = (nd[0].value,)   #the identifier
      return (nd[0].value,)            #the identifier

    # dclr --> ID '[' ']'
    if len(nd) == 2:
      nd.init_value = (nd[0].value, None)
      return (nd[0].value, None) 
      #      (identifier, arbitrary array size)

    # dclr --> ID '[' ICON ']'
    # identifier, fixed array size (python integer)
    nd.init_value = (nd[0].value, nd[2].value.value)
    return (nd[0].value, nd[2].value.value)
    #      (identifier, fixed int array size)

  def init_type(self, nd):
    '''Returns a XXXSymbol corresponding to the interpreter type 
    code representation for the child C++ type or class. Ancestor
    nodes can construct symbols directly using this return value
    as a constructor.'''
    checkNode(nd, 'init_type')
    # type --> CHAR | FLOAT | DOUBLE | INT
    # set type to one of string, float, int.
    # child will be of the form Node('CHAR', value=sym.StringSymbol)

    # if nd[0].label == 'CHAR':
    #   return sym.StringSymbol
    # if nd[0].label == 'DOUBLE' or nd[0].label == 'FLOAT':
    #   return sym.FloatSymbol
    # else: return sym.IntSymbol
    nd.init_value = nd[0].value
    return nd[0].value

  def init_func(self, nd):
    '''Returns a reference to the function symbol in the surrounding
    symbol table. Adds the function to the surrounding symbol table.'''
    checkNode(nd, 'init_func')
    # func --> fhead stmts '}'
    # This node needs a symbol table for the scope of the function.
    # We will eventually need to key functions in the symbol table
    # by their names and parameter types for overloading. (somehow)
    # Perhaps we can modify the FunctionSymbol class to accommodate
    # overloading.
    nd.initSymbolTable()
    fhead = self.descend(nd[0])    # the FunctionSymbol object
    fhead.func_node = nd
    nd.parent.put(fhead.id, fhead)
    if DEBUG:
      nd.printTable()
    # If the name of the function is `main', then store a pointer to this
    # node in the AST.
    if fhead.id == 'main':
      self.main = nd
    nd.init_value = fhead   # the pointer to the function in the symbol table
    return fhead

  def init_fhead(self, nd):
    '''Creates and returns a new function symbol.'''
    checkNode(nd, 'init_fhead')

    # fhead --> fname fargs '{' dcls
    # `fname' has the FunctionSymbol to modify.
    fname = self.descend(nd[0])    # the FunctionSymbol object
    fargs = self.descend(nd[1])    # the list of function parameters
    self.descend(nd[3])            # install the dcls symbols
    fname.args = fargs
    nd.init_value = fname   # the pointer to the function in the symbol table
    return fname

  def init_fname(self, nd):
    '''Create FunctionSymbol. If no type is given,
    type defaults to IntSymbol. Returns a pointer to the function in
    the symbol table.'''
    checkNode(nd, 'init_fname')

    # fname --> type ID
    #         | ID
    # associate type (XXXSymbol) with ID and store in nearest symbol table
    # (should be class or global (root) symbol table)
    if len(nd) == 2:
      return_type = self.descend(nd[0])
      identifier = nd[1].value
    else: 
      return_type = sym.IntSymbol
      identifier = nd[0].value
    s = sym.FunctionSymbol(identifier, ret=return_type)
    nd.init_value = s   # new function symbol 
    return s

  def init_fargs(self, nd):
    '''Returns a list of XXXSymbol instances, one for each argument
    in the order in which they appear.'''
    checkNode(nd, 'init_fargs')

    # fargs --> '(' ')'
    if len(nd) == 2:
      nd.init_value = []
      return []

    # fargs --> '(' args ')'
    args = self.descend(nd[1])
    nd.init_value = args
    return args

  def init_args(self, nd):
    '''Returns a list of XXXSymbol instances, one for each argument
    in the order in which they appear.'''
    checkNode(nd, 'init_args')

    # args --> type dclr
    if len(nd) == 2:
      # `type' nodes return a XXXSymbol after evaluation. Use
      # this as a constructor and then add to the symbol table.
      # Return the singleton list containing the new symbol.
      typ = self.descend(nd[0])      # XXXSymbol
      dclr = self.descend(nd[1])     # 1- or 2-tuple
      identifier = dclr[0]
      if len(dclr) == 1:
        # then just a simple type or class
        s = typ(identifier)
      else:
        # then dclr[1] has an array size
        s = sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1])
      nd.put(identifier, s)
      nd.init_value = [s]
      return [s]

    # args --> args ',' type dclr
    args = self.descend(nd[0])
    typ = self.descend(nd[2])
    dclr = self.descend(nd[3])
    identifier = dclr[0]
    if len(dclr) == 1:
      s = typ(identifier)
    else:
      s = sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1])
    nd.put(identifier, s)
    nd.init_value = args + [s]
    return args + [s]

  def init_block(self, nd):
    '''Create a prototype symbol table for this node.'''
    # block --> '{' stmts '}'
    nd.initSymbolTable()
    self.descend(nd[1])

  def init_stmts(self, nd):
    '''Descend into subtrees.'''
    # stmts -->
    # stmts --> stmts stmt
    for child in nd:
      self.descend(child)

  def init_stmt(self, nd):
    '''Descend into subtrees, creating prototype symbol tables
    where needed.'''
    # stmt --> ';'
    if not isinstance(nd[0], Node):
      return

    # stmt --> FOR '(' expro ';' cexpro ';' expro ')' stmt
    #   Create a proto symbol table for the current node. To do: Any declarations
    #   in the first expro clause will appear in this symbol table.
    if nd[0].value == 'for':
      nd.initSymbolTable()
      for child in nd:
        if isinstance(child, Node):
          self.descend(child)
      return

    # stmt --> block
    # stmt --> expr ';'
    # stmt --> IF '(' cexpr ')' stmt
    # stmt --> IF '(' cexpr ')' stmt ELSE stmt
    # stmt --> WHILE '(' cexpr ')' stmt
    # stmt --> DO stmt WHILE '(' cexpr ')' ';'
    # stmt --> CONTINUE ';'
    # stmt --> BREAK ';'
    # stmt --> RETURN ';'
    # stmt --> RETURN expr ';'
    #   In these cases, descend subtrees.
    for child in nd:
      if isinstance(child, Node):
        self.descend(child)

  def init_cexpro(self, nd):
    '''Not necessary to descend cexpro node.'''
    pass

  def init_cexpr(self, nd):
    '''Not necessary to descend cexpr node.'''
    pass

  def init_exprs(self, nd):
    '''Not necessary to descend exprs node.'''
    pass

  def init_expro(self, nd):
    '''Not necessary to descend expro node.'''
    pass

  def init_expr(self, nd):
    '''Not necessary to descend expr node.'''
    pass

  def init_lval(self, nd):
    '''Not necessary to descend lval node.'''
    pass

  def init_constant(self, nd):
    '''Not necessary to descend constant node.'''
    pass

  ########################################################################################
  #
  # SECOND PASS: PROGRAM EXECUTION FUNCTIONS
  #
  # These functions are of the form exec_XXX, where XXX is the label of
  # a node (a nonterminal).
  #

  def exec_prog(self, nd):
    checkNode(nd, 'exec_prog')

    # prog --> externs
    # Jump to main() and execute the function tree. Push the global
    # symbol table onto the stack, and then push the function symbol
    # table.
    fnode = self.main
    self.pushScope(nd.symtab)
    self.pushScope(fnode.symtab)
    val = self.execute(fnode)
    self.popScope()
    self.popScope()
    return val
    # Program finished!!!!

  def exec_externs(self, nd):
    '''Nothing to execute.'''
    pass

  def exec_extern(self, nd):
    '''Nothing to execute.'''
    pass

  def exec_dcls(self, nd):
    '''List of declarations. Nothing to execute.'''
    pass

  def exec_dcl(self, nd):
    '''Declaration. Nothing to execute.'''
    pass

  def exec_dclr(self, nd):
    '''Declarator. Nothing to execute.'''
    pass

  def exec_type(self, nd):
    '''Type expression. Not used in any executable productions.'''
    pass

  def exec_func(self, nd):
    '''During the execution phase, only the `stmts' child is relevant. Return either
    a XXXSymbol or None.'''
    checkNode(nd)

    # func --> fhead stmts '}'
    try:
      self.execute(nd[1])
    except ReturnSignal as signal:
      retval = signal.retval
      return retval
    else:
      return None

  def exec_fhead(self, nd):
    '''Function head in a declaration/definition. Nothing to execute.'''
    pass

  def exec_fname(self, nd):
    '''Function name in a declaration/definition. Nothing to execute.'''
    pass

  def exec_fargs(self, nd):
    '''Function arguments in a declaration/definition. Nothing to execute.'''
    pass

  def exec_args(self, nd):
    '''Function arguments in a declaration/definition. Nothing to execute.'''
    pass

  def exec_block(self, nd):
    checkNode(nd, 'exec_block')

    # block --> '{' stmts '}'
    # Enter a block. Push a new symbol table onto the stack.
    # Be careful! Check to see if there's a control flow signal so we can clean
    # up the scope we pushed.
    self.pushScope()
    try:
      self.execute(nd[1])
    finally:
      self.popScope()

  def exec_stmts(self, nd):
    checkNode(nd, 'exec_stmts')

    # stmts --> stmts stmt
    # Left recursion. Execute stmts then stmt.
    if len(nd) == 2:
      self.execute(nd[0])
      self.execute(nd[1])
      return

    # stmts -->
    # Do nothing.

  def exec_stmt(self, nd):
    checkNode(nd, 'exec_stmt')

    # stmt --> ';'
    # Empty statement. Simply return.
    if len(nd) == 1 and not isinstance(nd[0], Node) and nd[0].value == ';':
      return

    # stmt --> block
    # Enter a block. Block handles symbol table management.
    if len(nd) == 1:
      return self.execute(nd[0])

    # stmt --> expr ';'
    # Evaluate an expression. Nothing fancy.
    if len(nd) == 2 and nd[0].label == 'expr':
      return self.execute(nd[0])

    # SELECTION STATEMENTS
    # stmt --> IF '(' cexpr ')' stmt
    if len(nd) == 5 and nd[0].value == 'if':
      cond = self.execute(nd[2])
      if cond:
        return self.execute(nd[4])
      return

    # stmt --> IF '(' cexpr ')' stmt ELSE stmt
    if len(nd) == 7 and nd[0].value == 'if':
      cond = self.execute(nd[2])
      if cond:
        return self.execute(nd[4])
      return self.execute(nd[6])

    # ITERATION STATEMENTS
    # Iteration statements need to be very careful about enclosing calls to node functions
    # in try blocks. This is because they must handle ContinueSignals and BreakSignals.
    #
    # stmt --> WHILE '(' cexpr ')' stmt
    if len(nd) == 5 and nd[0].value == 'while':
      cond = self.execute(nd[2])
      while cond:
        try:
          stmt = self.execute(nd[4])  # stmt
        except ContinueSignal:
          pass
        except BreakSignal:
          break

        cond = self.execute(nd[2])    # condition
      return

    # stmt --> DO stmt WHILE '(' cexpr ')' ';'
    if len(nd) == 7 and nd[0].value == 'do':
      cond = True
      while cond:
        try:
          stmt = self.execute(nd[1])  # stmt
        except ContinueSignal:
          pass
        except BreakSignal:
          break

        cond = self.execute(nd[4])    # condition
      return

    # stmt --> FOR '(' expro ';' cexpro ';' expro ')' stmt
    #          [0] [1]  [2]  [3]   [4]  [5]  [6]  [7]  [8]
    if len(nd) == 9 and nd[0].value == 'for':

      # initializer 
      if nd[2] != None:
        self.execute(nd[2])

      # condition 
      if nd[4] == None:
        cond = True
      else:
        cond = self.execute(nd[4])

      # loop
      while cond:
        try:
          self.execute(nd[8])   # stmt
        except ContinueSignal:
          pass
        except BreakSignal:
          break

        # increment
        if nd[6] != None:
          self.execute(nd[6])
        # condition
        if nd[4] != None:
          cond = self.execute(nd[4])
      return

    # JUMP STATEMENTS
    # Jump statements require throwing control flow signal exceptions.
    #
    # stmt --> CONTINUE ';'
    if len(nd) == 2 and nd[0].value == 'continue':
      raise ContinueSignal()

    # stmt --> BREAK ';'
    if len(nd) == 2 and nd[0].value == 'break':
      raise BreakSignal()

    # stmt --> RETURN ';'
    if len(nd) == 2 and nd[0].value == 'return':
      raise ReturnSignal()

    # stmt --> RETURN expr ';'
    if len(nd) == 3 and nd[0].value == 'return':
      expr = self.execute(nd[1])
      raise ReturnSignal(expr)

  def exec_cexpro(self, nd):
    '''Evaluate a conditional expression (returning a Python boolean), or return 
    None if no expression exists.'''
    checkNode(nd, 'exec_cexpro')

    # cexpro --> cexpr
    if len(nd) == 1:
      return self.execute(nd[0])
    # cexpro -->
    return None

  def exec_cexpr(self, nd):
    '''Evaluate a conditional expression and return Python True or False.'''
    checkNode(nd, 'exec_cexpr')

    # cexpr --> expr
    # Return expr's boolean value. `expr' should be a XXXSymbol.
    if len(nd) == 1:
      return self.execute(nd[0]).boolean()

    # EXPRESSION COMPARISON
    # cexpr --> expr '==' expr
    # cexpr --> expr '!=' expr
    # cexpr --> expr '<=' expr
    # cexpr --> expr '>=' expr
    # cexpr --> expr '<' expr
    # cexpr --> expr '>' expr
    if len(nd) == 3 and nd[0].label == 'expr':
      expr1 = self.execute(nd[0])
      expr2 = self.execute(nd[2])
      op = nd[1]
      return expr1.oper(op, expr2)

    # BOOLEAN OPERATION
    # cexpr --> cexpr '&&' cexpr
    # cexpr --> cexpr '||' cexpr
    if len(nd) == 3 and nd[0].label == 'cexpr':
      if nd[1] == '&&':
        return self.execute(nd[0]) and self.execute(nd[2])
      return self.execute(nd[0]) or self.execute(nd[2]) 
    # cexpr --> '!' cexpr
    if len(nd) == 2:
      return not self.execute(nd[1])

  def exec_exprs(self, nd):
    '''Create and return a list of expressions (XXXSymbols).'''
    checkNode(nd, 'exec_exprs')

    # exprs --> exprs ',' expr
    # Left recursion. `exprs' is a list. Concatenate with the symbol returned
    # by `expr'. Return a list of XXXSymbols.
    if len(nd) == 3:
      exprs = self.execute(nd[0])
      expr = self.execute(nd[2])
      return exprs + [expr]

    # exprs --> expr
    # It's just a single expr, but the parent of this node expects a list to be returned.
    # So return the singleton list [expr].
    expr = self.execute(nd[0])
    return [expr]

  def exec_expro(self, nd):
    '''Evaluate the expression, or return None if there is no expression.'''
    checkNode(nd, 'exec_expro')

    # expro --> expr
    if len(nd) == 1:
      return self.execute(nd[0])
    # expro -->
    return None

  def exec_expr(self, nd):
    '''Evaluate an expression and return the value as a XXXSymbol. This node can
    indirectly derive a jump statement via function call. Set breakpoints where needed.
    '''
    checkNode(nd, 'exec_expr')

    # expr --> lval
    # expr --> constant
    # Just return the symbol pointed to by lval or constant.
    if len(nd) == 1:
      return self.execute(nd[0])

    # ASSIGNMENT OPERATIONS
    # expr --> lval '=' expr
    # expr --> lval '+=' expr
    # expr --> lval '-=' expr
    # expr --> lval '*=' expr
    # expr --> lval '/=' expr
    # expr --> lval '%=' expr
    # Evaluate both sides and call .oper().
    if len(nd) == 3 and isinstance(nd[0], Node) and nd[0].label == 'lval':
      lval = self.execute(nd[0])
      expr = self.execute(nd[2])
      op = nd[1]
      return lval.oper(op, expr)

    # BINARY OPERATIONS
    # expr --> expr '+' expr
    # expr --> expr '-' expr
    # expr --> expr '*' expr
    # expr --> expr '/' expr
    # expr --> expr '%' expr
    # expr --> expr '<<' expr
    # expr --> expr '>>' expr
    # Evaluate both sides and call .oper().
    if len(nd) == 3 and isinstance(nd[0], Node) and nd[0].label == 'expr':
      expr1 = self.execute(nd[0])
      expr2 = self.execute(nd[2])
      op = nd[1]
      return expr1.oper(op, expr2)

    # UNARY OPERATIONS
    # expr --> '-' expr
    # Evaluate expression and call .oper().
    if len(nd) == 2 and not isinstance(nd[0], Node) and nd[0] == '-':
      expr = self.execute(nd[1])
      op = '-'
      return expr.oper(op)

    # FUNCTION OPERATIONS
    # expr --> ID '(' ')'
    # Evaluate exprs if necessary and then call the function referenced by ID.
    # Be sure to push a new symbol table onto the stack. Manage breakpoints when
    # calling a function.
    if len(nd) == 3 and isinstance(nd[0], Node) and nd[0].label == 'ID':
      id = nd[0].value
      ### DEBUG OUTPUT FUNCTION (_dump())
      # dump the symbol table
      if id == '_dump':
        self.dump()
        return
      #####
      function = self.getSymbol(id)
      if function == None:
        raise err.VisError('[Interpreter] ERROR: Function "{}" has not been declared.'.format(id))
      fnode = function.func_node
      if fnode == None:
        raise err.VisError('[Interpreter] ERROR: Function "{}" has not been defined.'.format(id))

      self.pushScope(fnode.symtab)
      val = self.execute(fnode)
      self.popScope()
      return val

    # expr --> ID '(' exprs ')'
    # `exprs' should have returned a list of XXXSymbols.
    # After pushing a new scope but before entering the function ID, we should
    # add all of the exprs to the symbol table under their correct names. The
    # list of parameter IDs is given in the FunctionSymbol member `args'.
    if len(nd) == 4 and isinstance(nd[0], Node) and nd[0].label == 'ID':
      id = nd[0].value
      ### DEBUG OUTPUT FUNCTION:
      if id == '_print':
        exprs = self.execute(nd[2])
        for arg in exprs:
          print arg.value
        return
      ###
      function = self.getSymbol(id)
      if function == None:
        raise err.VisError('[Interpreter] ERROR: Function "{}" has not been declared.'.format(id))
      fnode = function.func_node
      if fnode == None:
        raise err.VisError('[Interpreter] ERROR: Function "{}" has not been defined.'.format(id))

      args = function.args    # list of XXXSymbols representing the function parameters in symtab 
      exprs = self.execute(nd[2])   # list of XXXSymbols to pass as arguments
      self.pushScope(fnode.symtab)
      # pass the arguments by putting them in the new symbol table. Make sure they
      # are COPIES of symbols. We just want their values.
      for arg,symbol in zip(args,exprs):
        symbol.id = arg.id
        self.putSymbol(arg.id, copy.deepcopy(symbol), force=True)
      val = self.execute(fnode)
      self.popScope()
      return val

    # expr --> '(' expr ')'
    # Simply evaluate the expr in parentheses.
    return self.execute(nd[1])

  def exec_lval(self, nd):
    '''Get the lval from the symbol stack. Return a pointer to the
    symbol in the symbol stack. An lval MUST have been declared, or
    there is an error in the user's code.'''
    checkNode(nd, 'exec_lval')

    # lval --> ID
    # Return a pointer to the XXXSymbol in the stack.
    if len(nd) == 1:
      id = nd[0].value
      lval = self.getSymbol(id)
      if lval == None:
        raise err.VisError('[Interpreter] ERROR: Identifier "{}" has not been declared'.format(id))
      return lval

    # lval --> ID '[' expr ']'
    # Not yet defined.

  def exec_constant(self, nd):
    '''Simply return the child XXXSymbol.'''
    checkNode(nd, 'exec_constant')

    # constant --> ICON | FCON | CCON | SCON
    return nd[0].value     # an XXXSymbol

#################################################################################

def main():
  # syntax tree for 5 + 7
  l1 = Node('ICON', value=5)
  l2 = Node('ICON', value=7)
  n = Node('expr', l1, '+', l2)

  print 'done.'

if __name__ == '__main__':
  main()