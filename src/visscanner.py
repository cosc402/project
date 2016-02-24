import vislexer

lexer = vislexer.Lexer()

print lexer.reserved
print lexer.tokens
lexer.build()

lexer.input(
  '''3 + 4 - 2
  int i;'''
)

for tok in lexer:
  print tok