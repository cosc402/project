class Node:
  def __init__(self, label, *children, **kwargs):
    self.label = label
    self.value = kwargs.get('value', None)
    self.children = children

  def __str__(self):
    chstr = [str(i) for i in self.children]
    chstr = ', '.join(chstr)
    return "Node {}: [{}]".format(self.label, chstr)

  def __iter__(self):
    return iter(self.children)

class Leaf:
  def __init__(self, label, val):
    self.label = label
    self.value = val

  def __str__(self):
    return "Leaf {}: {}".format(self.label, self.val)

class SyntaxTree:
  def __init__(self, root=None):
    self.root = root


def main():
  # syntax tree for 5 + 7
  l1 = Leaf('NUM', 5)
  l2 = Leaf('+', '+')
  l3 = Leaf('NUM', 7)

  expr = Node('expr', l1, l2, l3)

  print 'done.'

if __name__ == '__main__':
  main()