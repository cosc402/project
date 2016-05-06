####################################################
# delete_comment.py
# 
# Receives a C/C++ source file as input and strips
# away the comments. Dumps to stdout.
#
####################################################

import sys
import re

if len(sys.argv) != 2:
  print 'Please provide an input file.'
  exit(1)

fin = open(sys.argv[1])
in_block = False

for line in fin:
  l = line
  pound = line.strip().find('#')
  using = line.strip().find('using ')

  while True:
    slash = l.find('//')
    block_begin = l.find('/*')
    block_end = l.find('*/')

    if not in_block:
      if pound == 0 or using == 0: 
        l = ''
        break
      if slash != -1 and (block_begin == -1 or slash < block_begin):
        l = l[:slash]
        break
      if block_begin != -1:
        if block_end == -1:
          l = l[:block_begin]
          in_block = True
          break
        l = l[:block_begin] + ' ' + l[block_end+2:]
        continue
      break

    else:
      if block_end == -1:
        l = ''
        break
      l = ' ' + l[block_end+2:]
      in_block = False

  sys.stdout.write(l)
