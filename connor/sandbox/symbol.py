import viserror

class Symbol:

  def __init__(self, name, _type, value=None):
    self.value = value
    self.type = _type
    self.name = name

  def __str__(self):
    return '{} ({}): {}'.format(self.name, self.type, self.value)

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