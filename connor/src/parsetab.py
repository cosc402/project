
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '10E81422F91BC07721C006054916BBD5'
    
_lr_action_items = {'INSERT':([1,],[10,]),'*':([13,16,17,18,21,22,23,29,31,32,33,34,35,],[-17,-16,25,-18,25,25,-14,25,-15,25,-12,25,-13,]),'COUT':([0,],[1,]),'INT':([0,],[3,]),'DOUBLE':([0,],[2,]),'+':([13,16,17,18,21,22,23,29,31,32,33,34,35,],[-17,-16,24,-18,24,24,-14,24,-15,-10,-12,-11,-13,]),'FLOAT':([0,],[4,]),'CHARACTER':([10,12,14,15,20,24,25,26,27,],[13,13,13,13,13,13,13,13,13,]),'/':([13,16,17,18,21,22,23,29,31,32,33,34,35,],[-17,-16,27,-18,27,27,-14,27,-15,27,-12,27,-13,]),'CHAR':([0,],[5,]),')':([13,16,18,22,23,31,32,33,34,35,],[-17,-16,-18,31,-14,-15,-10,-12,-11,-13,]),'NUM':([10,12,14,15,20,24,25,26,27,],[16,16,16,16,16,16,16,16,16,]),'BOOL':([0,],[6,]),'-':([10,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,29,31,32,33,34,35,],[15,15,-17,15,15,-16,26,-18,15,26,26,-14,15,15,15,15,26,-15,-10,-12,-11,-13,]),'(':([10,12,14,15,20,24,25,26,27,],[14,14,14,14,14,14,14,14,14,]),';':([11,13,16,17,18,21,23,29,31,32,33,34,35,],[19,-17,-16,28,-18,30,-14,36,-15,-10,-12,-11,-13,]),'=':([9,11,],[12,20,]),'ID':([0,2,3,4,5,6,8,10,12,14,15,20,24,25,26,27,],[9,-6,-5,-7,-8,-9,11,18,18,18,18,18,18,18,18,18,]),'$end':([7,19,28,30,36,],[0,-4,-3,-1,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([10,12,14,15,20,24,25,26,27,],[17,21,22,23,29,32,33,34,35,]),'statement':([0,],[7,]),'declaration':([0,],[8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> ID = expression ;','statement',4,'p_statement_assign','visparser.py',19),
  ('statement -> declaration ID = expression ;','statement',5,'p_statement_decl_assign','visparser.py',23),
  ('statement -> COUT INSERT expression ;','statement',4,'p_statement_cout','visparser.py',27),
  ('statement -> declaration ID ;','statement',3,'p_statement_decl','visparser.py',31),
  ('declaration -> INT','declaration',1,'p_decl_var','visparser.py',35),
  ('declaration -> DOUBLE','declaration',1,'p_decl_var','visparser.py',36),
  ('declaration -> FLOAT','declaration',1,'p_decl_var','visparser.py',37),
  ('declaration -> CHAR','declaration',1,'p_decl_var','visparser.py',38),
  ('declaration -> BOOL','declaration',1,'p_decl_var','visparser.py',39),
  ('expression -> expression + expression','expression',3,'p_expression_binop','visparser.py',43),
  ('expression -> expression - expression','expression',3,'p_expression_binop','visparser.py',44),
  ('expression -> expression * expression','expression',3,'p_expression_binop','visparser.py',45),
  ('expression -> expression / expression','expression',3,'p_expression_binop','visparser.py',46),
  ('expression -> - expression','expression',2,'p_expression_uminus','visparser.py',53),
  ('expression -> ( expression )','expression',3,'p_expression_group','visparser.py',57),
  ('expression -> NUM','expression',1,'p_expression_number','visparser.py',61),
  ('expression -> CHARACTER','expression',1,'p_expression_character','visparser.py',65),
  ('expression -> ID','expression',1,'p_expression_id','visparser.py',69),
]
