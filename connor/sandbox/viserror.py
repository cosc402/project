class VisError(Exception):
  '''Base class for Visualizer exceptions.'''
  pass

class VisTypeError(VisError):
  '''Exception raised for type errors.

  Attributes:
      msg -- explanation of the error
      type -- name of problem type
  '''

  def __init__(self, _type, msg=''):
    self.msg = msg
    self.type = _type