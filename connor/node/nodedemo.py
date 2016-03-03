import nodelexer
import nodeparser
import node

def main():
  lexer = nodelexer.Lexer()
  lexer.build()
  parser = nodeparser.Parser(lexer.tokens)
  parser.build()

  while True:
    try:
      s = raw_input('> ')
      if s.strip() == 'quit()':
        break
    except EOFError:
      break
    if not s: continue
    parser.parse(s)

if __name__ == '__main__':
  main()