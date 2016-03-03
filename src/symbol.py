#--------------------------------------------------
# symbol.py
#
# Defines two classes:
#
#   Symbol -- a symbol table entry. Has attributes
#     .value -- If the token is an ID, this stores the ID's value
#               in memory.
#     .type  -- token type/tag ('INT', 'ID', etc.)
#     .name  -- lexeme that corresponds to the token. If the token
#               was an ID, then the name corresponds to the variable
#               name.
#     
#   Env -- You can think of an Env object as a symbol table. It is
#          meant to be linked to its parent symbol tables in a
#          tree-like structure. Has attributes
#     .table -- a hash table keyed on strings that represent the names
#               of identifiers. It maps these strings to symbol table
#               entries of class Symbol (above).
#     .prev  -- a "pointer" (i.e. regular variable in Python) to this
#               environment's parent Env structure
#   Env methods
#     .put(name, type, val=None)
#     .update(name, val)
#     .get(name)
#     .print_table()
#
#---------------------------------------------------

import viserror

#--------------
# class Symbol
#

class Symbol:
  def __init__(self, name, _type, value=None):
    self.value = value
    self.type = _type
    self.name = name

  def __str__(self):
    return '{} ({}): {}'.format(self.name, self.type, self.value)

#-----------
# class Env
#

class Env:
  def __init__(self, p=None):
    # Symbol table for this scope
    self.table = {}

    # Pointer to surrounding (parent) scope
    self.prev = p

  def put(self, name, _type, val=0):
    if name in self.table:
      raise viserror.VisError
    sym = Symbol(name, _type, val)
    self.table[name] = sym

  def update(self, name, val):
    if name not in self.table:
      print '**Syntax Error**: identifier {} not declared'.format(name)
      raise viserror.VisError
    self.table[name].value = val

  def get(self, name):
    if name in self.table:
      return self.table[name]
    else:
      print '**VisError**: {} does not exist in symbol table'

  def print_table(self):
    print 'Symbol table:'
    for sym in self.table.values():
      print sym

#=============================================
#### For testing: ####

def main():
  print 'hello world'
  e = Env()
  # int i = 5;
  e.put('i', Symbol('i','INT',5))
  # int j = 6;
  e.put('j', Symbol('j','INT',6))

  for s in e.table:
    print e.table[s]

if __name__ == '__main__':
  main()
