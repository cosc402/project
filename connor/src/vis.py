#-----------------------------------------------------------
# vis.py
#
# C++ interpreter driver
#-----------------------------------------------------------

import vislexer
import visparser

def main():
  lexer = vislexer.Lexer()
  lexer.build()
  parser = visparser.Parser(lexer.tokens)
  parser.build()

  while True:
    try:
      s = raw_input('test > ')
      if s == 'quit()':
        break
    except EOFError:
      break
    if not s: continue

    parser.parse(s)
    parser.headsym.print_table()

if __name__ == '__main__':
  main()