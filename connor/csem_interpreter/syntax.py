import symbol as sym
import viserror as err

global DEBUG

#
# Node
#
# A node in the parse tree. This represents a
# nonterminal in the syntax tree produced by PLY.
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

  # *** Maybe use get() to get a pointer to the entry
  #     and manipulate that instead... ***
  # update the value of an entry in the symbol table
  # associated with the closest ancestor of this node
  # def update(self, id, val):
  #   if self.symtab == None:
  #     if self.parent == None:
  #       raise err.VisError('"{}" does not exist in any symbol table.'.format(name))
  #     else:
  #       self.parent.update(id, val)
  #   else:
  #     self.symtab.update(id, val)

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
      if level < 0:
        print '=========================================='
        print 'Scope = {}'.format(level)
        print '------------------------------------------'
      for sym in nd.symtab.table.values():
        print '  ', sym
      level -= 1
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
    self.stop = True      # controls where the step() function returns

    self.node_funcs = {
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
      'lblstmt':          self.init_lblstmt,
      'labels':           self.init_labels,
      'stmt':             self.init_stmt,
      'cexpro':           self.init_cexpro,
      'cexpr':            self.init_cexpr,
      'exprs':            self.init_exprs,
      'expro':            self.init_expro,
      'expr':             self.init_expr,
      'lval':             self.init_lval,
      'constant':         self.init_constant
    }

  def printTree(self, nd=None, level=0):
    if nd == None:
      nd = self.root
    if not isinstance(nd, Node):
      print '{}leaf {}'.format(' '*level, nd)
      return 
    print '{}node {}'.format(' '*level, nd.label)
    for child in nd:
      self.printTree(child, level+2)

  def step(self):
    self.descend(self.root)

  # Wrapper for calling the node rules.
  # Execute/evaluate the subtree with root `nd'.
  def descend(self, nd=None):
    if nd == None: nd = self.cur
    return self.node_funcs[nd.label](nd)

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
  # The result of all of these functions is to initialize symbol
  # tables and attach them to the nodes that represent scopes.
  # Once this pass has been made, the interpreter is ready to
  # execute the program using the rules defined in the
  # `exec_XXX()' functions.
  #

  def init_prog(self, nd):
    checkNode(nd, 'init_prog')
    # prog --> externs
    # This is the start symbol. This node will house the
    # global symbol table.
    nd.initSymbolTable()
    self.descend(nd.children[0])
    print 'initial descent complete'

  def init_externs(self, nd):
    checkNode(nd, 'init_externs')
    # externs --> 
    #           | externs extern
    for child in nd.children:
      self.descend(child)

  def init_extern(self, nd):
    checkNode(nd, 'init_extern')
    # extern --> dcl ';'
    #          | func
    for child in nd.children:
      if isinstance(child, Node):
        self.descend(child)

  def init_dcls(self, nd):
    checkNode(nd, 'init_dcls')
    # dcls -->
    #        | dcls dcl ';'
    for child in nd.children:
      if isinstance(child, Node):
        self.descend(child)

  def init_dcl(self, nd):
    '''Returns a XXXSymbol object to carry the type across a
    comma-separated list of declarations.'''
    checkNode(nd, 'init_dcl')

    # dcl --> type dclr
    # `type' nodes return a XXXSymbol after evaluation. Use
    # this as a constructor and then add to the symbol table.
    if len(nd.children) == 2:
      typ = self.descend(nd.children[0])      # XXXSymbol
      dclr = self.descend(nd.children[1])     # 1- or 2-tuple
      identifier = dclr[0]
      if len(dclr) == 1:
        nd.put(identifier, typ(identifier))
      else:
        nd.put(identifier, sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1]))
      return typ

    # dcl --> dcl ',' dclr
    # The type that should be carried over into the other dclr is obtained
    # from descending the `dcl' child.
    typ = self.descend(nd.children[0])
    dclr = self.descend(nd.children[2])
    identifier = dclr[0]
    if len(dclr) == 1:
      nd.put(identifier, typ(identifier))
    else:
      nd.put(identifier, sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1]))
    return typ

  def init_dclr(self, nd):
    '''Returns either a 1- or 2-tuple, depending on the subtree.
    If dclr --> ID
      return ("identifier",)
    If dclr --> ID '[' ']'        // second element None indicates array of unknown size
      return ("identifier", None)
    If dclr --> ID '[' ICON ']'
      return ("identifier", size of array)'''
    checkNode(nd, 'init_dclr')

    # dclr --> ID
    if len(nd.children) == 1:
      return (nd.children[0].value,) #identifier

    # dclr --> ID '[' ']'
    if len(nd.children) == 2:
      return (nd.children[0].value, None) #identifier, arbitrary array size

    # dclr --> ID '[' ICON ']'
    # identifier, fixed array size
    return (nd.children[0].value, nd.children[2].value.value)

  def init_type(self, nd):
    '''Returns a XXXSymbol corresponding to the interpreter type 
    code representation for the child C++ type or class. Ancestor
    nodes can construct symbols directly using this return value
    as a constructor.'''
    checkNode(nd, 'init_type')
    # type --> CHAR | FLOAT | DOUBLE | INT
    # set type to one of string, float, int.
    # child will be of the form Node('CHAR', value=sym.StringSymbol)

    # if nd.children[0].label == 'CHAR':
    #   return sym.StringSymbol
    # if nd.children[0].label == 'DOUBLE' or nd.children[0].label == 'FLOAT':
    #   return sym.FloatSymbol
    # else: return sym.IntSymbol
    return nd.children[0].value

  def init_func(self, nd):
    '''Returns a reference to the function symbol in the surrounding
    symbol table. Adds the function to the surrounding symbol table.'''
    checkNode(nd, 'init_func')
    # func --> fhead stmts '}'
    # This node needs a symbol table for the scope of the function.
    # We will eventually need to key functions in the symbol table
    # by their names and parameter types. (somehow)
    # Perhaps we can modify the FunctionSymbol class to accommodate
    # overloading.
    nd.initSymbolTable()
    fhead = self.descend(nd.children[0])    # the FunctionSymbol object
    fhead.func_node = nd
    nd.parent.put(fhead.id, fhead)
    nd.printTable()
    return fhead

  def init_fhead(self, nd):
    '''Creates and returns a new function symbol.'''
    checkNode(nd, 'init_fhead')

    # fhead --> fname fargs '{' dcls
    # `fname' carries the FunctionSymbol to modify.
    fname = self.descend(nd.children[0])    # the FunctionSymbol object
    fargs = self.descend(nd.children[1])    # the list of function parameters
    self.descend(nd.children[3])            # install the dcls symbols
    fname.args = fargs
    return fname

  def init_fname(self, nd):
    '''Create FunctionSymbol. If no type is given,
    type defaults to INT. Returns a pointer to the function in
    the symbol table.'''
    checkNode(nd, 'init_fname')

    # fname --> type ID
    #         | ID
    # associate type (XXXSymbol) with ID and store in nearest symbol table
    # (should be class or global (root) symbol table)
    if len(nd.children) == 2:
      return_type = self.descend(nd.children[0])
      identifier = nd.children[1].value
    else: 
      return_type = sym.IntSymbol
      identifier = nd.children[0].value
    return sym.FunctionSymbol(identifier, ret=return_type)

  def init_fargs(self, nd):
    '''This should return a list of XXXSymbol instances, one for each
    argument.'''
    checkNode(nd, 'init_fargs')

    # fargs --> '(' ')'
    if len(nd.children) == 2:
      return []

    # fargs --> '(' args ')'
    return self.descend(nd.children[1])

  def init_args(self, nd):
    '''This should return a list of XXXSymbol instances, one for each
    argument.'''
    checkNode(nd, 'init_args')

    # args --> type dclr
    if len(nd.children) == 2:
      # `type' nodes return a XXXSymbol after evaluation. Use
      # this as a constructor and then add to the symbol table.
      # Return the singleton list containing the new symbol.
      typ = self.descend(nd.children[0])      # XXXSymbol
      dclr = self.descend(nd.children[1])     # 1- or 2-tuple
      identifier = dclr[0]
      if len(dclr) == 1:
        s = typ(identifier)
      else:
        s = sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1])
      nd.put(identifier, s)
      return [s]

    # args --> args ',' type dclr
    args = self.descend(nd.children[0])
    typ = self.descend(nd.children[2])
    dclr = self.descend(nd.children[3])
    identifier = dclr[0]
    if len(dclr) == 1:
      s = typ(identifier)
    else:
      s = sym.VectorSymbol(identifier, contains=typ, maxlen=dclr[1])
    nd.put(identifier, s)
    return args + [s]

  def init_block(self, nd):
    pass

  def init_stmts(self, nd):
    pass

  def init_lblstmt(self, nd):
    pass

  def init_labels(self, nd):
    pass

  def init_stmt(self, nd):
    pass

  def init_cexpro(self, nd):
    pass

  def init_cexpr(self, nd):
    pass

  def init_exprs(self, nd):
    pass

  def init_expro(self, nd):
    pass

  def init_expr(self, nd):
    pass

  def init_lval(self, nd):
    pass

  def init_constant(self, nd):
    pass

def main():
  # syntax tree for 5 + 7
  l1 = Node('ICON', value=5)
  l2 = Node('ICON', value=7)
  n = Node('expr', l1, '+', l2)

  print 'done.'

if __name__ == '__main__':
  main()