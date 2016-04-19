import viserror

# ABOUT TYPE CODES:
#
# Type codes are strings that should match the case and spelling
# of the appropriate type as found in the C++ code. For example,
# if the input has "int x;", then insert the IntSymbol x into the
# symbol table with .type = 'int'.

#
# Symbol
# (ABSTRACT)
#
# Superclass for all symbol table entries. Do not use Symbol,
# only derived classes. Every derived class must implement
#
#   update(value)
#     - update the symbol's value
#   oper(op_code, rhs)
#     - as in C++, "overload" the operator given by op_code
#       for various types (deduce the type from rhs, a XXXSymbol object).
#       oper() should return a XXXSymbol object with the new type and
#       value. (use __class__ if necessary)
#
# Types: For XXXSymbol, use XXXType.
#
# Identifiers: An "anonymous" symbol should be used to propogate a
#     value up the AST. An anonymous symbol is one whose id = None
#     and one that is not stored in any symbol table.
#
class Symbol:
  def __init__(self, id, value=None):
    self.id = id
    self.value = value
    self.type = None

  def __str__(self):
    return '{} ({}): {}'.format(self.id, self.type, self.value)

  def update(self, value):
    self.value = value

  # it is necessary to override this! oper() is called by the
  # AST in syntax.py to figure out how to evaluate expressions.
  # When checking the type of `rhs', just be sure to check
  # what class `rhs' is an instance of. It should be an instance
  # of a class XXXSymbol.
  #
  # If rhs = None, then treat op_code as a unary operation.
  def oper(self, op_code, rhs=None):
    pass

class IntSymbol(Symbol):
  def __init__(self, id, value=0):
    Symbol.__init__(self, id, value)
    self.type = 'int'

  def oper(self, op_code, rhs=None):
    # int relop any
    if rhs != None:
      if op_code == '==':
        return IntSymbol(None, self.value == rhs.value)
      if op_code == '!=':
        return IntSymbol(None, self.value != rhs.value)
      if op_code == '<=':
        return IntSymbol(None, self.value <= rhs.value)
      if op_code == '>=':
        return IntSymbol(None, self.value >= rhs.value)
      if op_code == '<':
        return IntSymbol(None, self.value < rhs.value)
      if op_code == '>':
        return IntSymbol(None, self.value > rhs.value)
      if op_code == '&&':
        return IntSymbol(None, self.value and rhs.value)
      if op_code == '||':
        return IntSymbol(None, self.value or rhs.value)

    # int op int
    if isinstance(rhs, IntSymbol):
      if op_code == '+':
        return IntSymbol(None, self.value + rhs.value)
      if op_code == '-':
        return IntSymbol(None, self.value - rhs.value)
      if op_code == '*':
        return IntSymbol(None, self.value * rhs.value)
      if op_code == '/':
        return IntSymbol(None, self.value / rhs.value)
      if op_code == '%':
        return IntSymbol(None, self.value % rhs.value)
      if op_code == '=':
        self.value = rhs.value
        return self
      if op_code == '+=':
        self.value += rhs.value
        return self
      if op_code == '-=':
        self.value -= rhs.value
        return self
      if op_code == '*=':
        self.value *= rhs.value
        return self
      if op_code == '/=':
        self.value /= rhs.value
        return self
      if op_code == '%=':
        self.value %= rhs.value
        return self

    # int op float
    if isinstance(rhs, FloatSymbol):
      if op_code == '+':
        return FloatSymbol(None, self.value + rhs.value)
      if op_code == '-':
        return FloatSymbol(None, self.value - rhs.value)
      if op_code == '*':
        return FloatSymbol(None, self.value * rhs.value)
      if op_code == '/':
        return FloatSymbol(None, self.value / rhs.value)

    # op int
    if rhs == None:
      if op_code == '-':
        return IntSymbol(None, -self.value)
      if op_code == '!':
        return IntSymbol(None, not self.value)
      if op_code == '++':
        self.value += 1
        return IntSymbol(None, self.value-1)
      if op_code == '--':
        self.value -= 1
        return IntSymbol(None, self.value+1)

    return None

class FloatSymbol(Symbol):
  def __init__(self, id, value=0.0):
    Symbol.__init__(self, id, value)
    self.type = 'float'

  def oper(self, op_code, rhs):
    # float relop any
    if rhs != None:
      if op_code == '==':
        return IntSymbol(None, self.value == rhs.value)
      if op_code == '!=':
        return IntSymbol(None, self.value != rhs.value)
      if op_code == '<=':
        return IntSymbol(None, self.value <= rhs.value)
      if op_code == '>=':
        return IntSymbol(None, self.value >= rhs.value)
      if op_code == '<':
        return IntSymbol(None, self.value < rhs.value)
      if op_code == '>':
        return IntSymbol(None, self.value > rhs.value)
      if op_code == '&&':
        return IntSymbol(None, self.value and rhs.value)
      if op_code == '||':
        return IntSymbol(None, self.value or rhs.value)

    # float op int/float
    if isinstance(rhs, IntSymbol) or isinstance(rhs, FloatSymbol):
      if op_code == '+':
        return FloatSymbol(None, self.value + rhs.value)
      if op_code == '-':
        return FloatSymbol(None, self.value - rhs.value)
      if op_code == '*':
        return FloatSymbol(None, self.value * rhs.value)
      if op_code == '/':
        return FloatSymbol(None, self.value / rhs.value)
      if op_code == '%':
        return FloatSymbol(None, self.value % rhs.value)
      if op_code == '=':
        self.value = rhs.value
        return self
      if op_code == '+=':
        self.value += rhs.value
        return self
      if op_code == '-=':
        self.value -= rhs.value
        return self
      if op_code == '*=':
        self.value *= rhs.value
        return self
      if op_code == '/=':
        self.value /= rhs.value
        return self
      if op_code == '%=':
        self.value %= rhs.value
        return self

    # op float
    if rhs == None:
      if op_code == '-':
        return FloatSymbol(None, -self.value)
      if op_code == '!':
        return FloatSymbol(None, not self.value)
      if op_code == '++':
        self.value += 1
        return FloatSymbol(None, self.value-1)
      if op_code == '--':
        self.value -= 1
        return FloatSymbol(None, self.value+1)

    return None

# i don't think i'll need char, but just in case...
class CharSymbol(Symbol):
  def __init__(self, id, value=''):
    Symbol.__init__(self, id, value)
    self.type = 'char'

class StringSymbol(Symbol):
  def __init__(self, id, value=''):
    Symbol.__init__(self, id, value)
    self.type = 'string'

  def oper(self, op_code, rhs):
    # string op string
    if isinstance(rhs, StringSymbol):
      if op_code == '+':
        return StringSymbol(None, self.value + rhs.value)
      if op_code == '=':
        self.value = rhs.value
        return self
      if op_code == '+=':
        self.value += rhs.value
        return self

  def length(self):
    return IntSymbol(None, len(self.value))

  def clear(self):
    self.value = ''

  def empty(self):
    return len(self.value) == 0

# 
# VectorSymbol
#
# kwargs:
#   value -- a list (default: [])
#   dim -- dimension (default: 1)
#   contains -- data type of contents, in the form of a XXXSymbol class 
#               reference (what is the data type at the last level of
#               indirection?) (default: IntSymbol)
#   
class VectorSymbol(Symbol):
  def __init__(self, id, **kwargs):
    value = kwargs.get('value', [])
    Symbol.__init__(self, id, value)
    self.dim = kwargs.get('dim', 1)
    self.maxlen = kwargs.get('maxlen', 0)
    self.contains = kwargs.get('contains', IntSymbol)
    self.type = 'VECTOR({}, {})'.format(self.dim, self.contains)

  def oper(self, op_code, rhs=None):
    pass

  def length(self):
    return IntSymbol(None, len(self.value))
  # implement vector methods and stuff

# value should probably be a pointer to the node that begins
# the function's first statement
class FunctionSymbol(Symbol):
  def __init__(self, id, **kwargs):
    value = kwargs.get('value', None)
    Symbol.__init__(self, id, value)
    self.return_type = kwargs.get('ret', None)

    # list of string identifiers.
    # actual XXXSymbols should be stored in the closest symbol table.
    self.args = kwargs.get('args', [])    

    # reference to the node in the syntax tree that defines the function
    self.func_node = kwargs.get('func_node', None)

  def __str__(self):
    return '{} (function, {}) {}: {}'.format(
      self.id, self.return_type, self.args, self.value)

  # when a function is called and is used in an expression, the
  # interpreter's responsibility is to use the operation defined
  # by self.return_type. For instance, if this FunctionSymbol is
  # int max(int a, int b), then the interpreter will simply call
  # IntSymbol.oper(), or something like that.
  def oper(self, op_code, rhs=None):
    pass

class Env:
  def __init__(self):
    # Symbol table (one scope)
    self.table = {}

  def put(self, name, symobj):
    if name in self.table:
      raise viserror.VisError('Identifier {} already declared'.format(name))
    self.table[name] = symobj

  # *** deprecated. update is now handled by XXXSymbol classes ***
  # def update(self, name, val):
  #   if name not in self.table:
  #     return
  #   self.table[name].value = val

  # returns a reference to the symbol entry for `name'.
  # If it doesn't exist, returns None
  def get(self, name):
    if name in self.table:
      return self.table[name]
    else: return None

  def printTable(self):
    print 'Symbol table:'
    for sym in self.table.values():
      print sym

#### For testing: ####

def main():
  print 'hello world'
  e = Env()
  # int i = 5;
  e.put('i', IntSymbol('i', 5))
  # int j = 6;
  e.put('j', IntSymbol('i', 6))

  for s in e.table:
    print e.table[s]

if __name__ == '__main__':
  main()