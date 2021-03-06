# gloabl
DEBUG = False

import symbol
import viserror
import csemlexer
import csemparser
import sys
from syntax import *

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
  if DEBUG: ast.printTree()

  ast.init()
  ast.execute()

if __name__ == '__main__':
  main()