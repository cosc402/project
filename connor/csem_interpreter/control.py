#
# ControlFlowSignal(destnode, retval=None) : Exception
# (ABSTRACT)
#
# If the interpreter needs to execute a jump statement, then the statement
# that issues the jump should throw a subclass of this exception. If a node can
# derive a jump statement (return, break, etc.), then the node should enclose
# statements that descend into the syntax tree in try blocks. Depending on the
# exception that is caught, a node rule may want to take certain steps to clean
# up (push/pop symbol tables, etc.) before yielding control.
#
# MEMBERS
#
#   destnode : A reference to the Node to which control should be yielded.
#
class ControlFlowSignal(Exception):
  def __init__(self):
    pass

class ContinueSignal(ControlFlowSignal):
  def __init__(self):
    pass

class BreakSignal(ControlFlowSignal):
  def __init__(self):
    pass

class ReturnSignal(ControlFlowSignal):
  def __init__(self, retval=None):
    self.retval = retval    # should be an XXXSymbol

#
# Breakpoint(node, type)
#
# Objects that belong in the callstack. A breakpoint may be any Node to which
# control might be abruptly yielded. For instance, a `func' Node would get
# control after a return statement is executed. A selection statement Node
# would get control after a break statement is executed. The type of
# breakpoint determines which types of jump statements the Node would accept
# to retake control.
#
# MEMBERS
#
#   node : A reference to the Node for which this breakpoint applies.
#
#   type : A string with a special code that describes the type of breakpoint.
#
# TYPE CODES
#
#   The following strings are acceptable type codes for use in the `type' member:
#
#       loop_begin : accepts
#         ContinueSignal
#
#       loop_end : accepts
#         BreakSignal
#
#       func : accepts
#         ReturnSignal
#
class Breakpoint:
  def __init__(self, node, type):
    self.node = node
    self.type = type
