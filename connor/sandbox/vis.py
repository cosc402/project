import vislexer
import visscanner

def main():
  lexer = vislexer.Lexer()
  lexer.build()
  parser = visscanner.Parser()
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