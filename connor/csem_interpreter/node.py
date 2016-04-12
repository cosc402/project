import symbol
import viserror as err

#
# Node
#
# A node in the parse tree. This represents a
# nonterminal in the syntax tree produced by PLY.
#
class Node:
  def __init__(self, label, *children, **kwargs):
    self.parent = None
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
      self.symtab = Env()
    else:
      self.symtab = symtab

  # insert an identifier-value pair into the symbol table
  # associated with this node
  def put(self, name, type, val=0):
    self.symtab.put(name, type, val)

  # update the value of a symbol table entry
  def update(self, name, val):
    self.symtab.update(name, val)

  # retrieve the value associated with the symbol table entry
  def get(self, name):
    self.symtab.get(name)

  # dump this node's symbol table
  def printTable(self):
    self.symtab.printTable()
###############################################################

#
# SyntaxTree
#
# Structure that should contain the AST after the parser returns.
# Defines traversal operations.
#
class SyntaxTree:
  def __init__(self, root=None):
    self.root = root
    self.cur = root
    self.stop = True      # controls where the step() function returns

    self.node_funcs = {
      'prog':             self.ast_prog,
      'externs':          self.ast_externs,
      'extern':           self.ast_extern,
      'dcls':             self.ast_dcls,
      'dcl':              self.ast_dcl,
      'dclr':             self.ast_dclr,
      'type':             self.ast_type,
      'func':             self.ast_func,
      'fhead':            self.ast_fhead,
      'fname':            self.ast_fname,
      'fargs':            self.ast_fargs,
      'args':             self.ast_args,
      'block':            self.ast_block,
      'stmts':            self.ast_stmts,
      'lblstmt':          self.ast_lblstmt,
      'labels':           self.ast_labels,
      'stmt':             self.ast_stmt,
      'cexpro':           self.ast_cexpro,
      'cexpr':            self.ast_cexpr,
      'exprs':            self.ast_exprs,
      'expro':            self.ast_expro,
      'expr':             self.ast_expr,
      'lval':             self.ast_lval,
      'constant':         self.ast_constant
    }

  def printTree(self, nd, level=0):
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

  #########################
  # 
  # Node Functions
  #
  # Each of these functions takes an AST node as a parameter
  # and each must return a result (return `None' if no value
  # should be returned). The function `ast_XXX' descends into
  # the subtree whose root is the node `nd', where nd.label
  # must be 'XXX'. If the label does not match, bad things
  # surely await you.
  #

  def ast_prog(self, nd):
    # prog --> externs
    self.descend(nd.children[0])

  def ast_externs(self, nd):
    pass

  def ast_extern(self, nd):
    pass

  def ast_dcls(self, nd):
    pass

  def ast_dcl(self, nd):
    pass

  def ast_dclr(self, nd):
    pass

  def ast_type(self, nd):
    pass

  def ast_func(self, nd):
    pass

  def ast_fhead(self, nd):
    pass

  def ast_fname(self, nd):
    pass

  def ast_fargs(self, nd):
    pass

  def ast_args(self, nd):
    pass

  def ast_block(self, nd):
    pass

  def ast_stmts(self, nd):
    pass

  def ast_lblstmt(self, nd):
    pass

  def ast_labels(self, nd):
    pass

  def ast_stmt(self, nd):
    pass

  def ast_cexpro(self, nd):
    pass

  def ast_cexpr(self, nd):
    pass

  def ast_exprs(self, nd):
    pass

  def ast_expro(self, nd):
    pass

  def ast_expr(self, nd):
    pass

  def ast_lval(self, nd):
    pass

  def ast_constant(self, nd):
    pass

def main():
  # syntax tree for 5 + 7
  l1 = Node('ICON', value=5)
  l2 = Node('ICON', value=7)
  n = Node('expr', l1, '+', l2)

  print 'done.'

if __name__ == '__main__':
  main()