import symbol
import viserror
import csemlexer
import csemparser
import sys
from syntax import *

# gloabl
DEBUG = True

def main():
  if len(sys.argv) != 2:
    print 'Please supply input source file.'
    exit(1)

  lexer = csemlexer.Lexer()
  lexer.build()
  parser = csemparser.Parser(lexer.tokens)
  parser.build()

  fin = open(sys.argv[1])
  parser.parse(fin.read())

  ast = parser.ast
  ast.printTree()

  ast.init()

if __name__ == '__main__':
  main()