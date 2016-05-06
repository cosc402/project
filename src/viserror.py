class VisError(Exception):
  '''Base class for Visualizer exceptions.'''
  def __init__(self, value='VisError'):
    self.value = value

  def __str__(self):
    return str(self.value)

class VisTypeError(VisError):
  '''Exception raised for type errors.

  Attributes:
      msg -- explanation of the error
      type -- name of problem type
  '''

  def __init__(self, _type, msg=''):
    self.msg = msg
    self.type = _type