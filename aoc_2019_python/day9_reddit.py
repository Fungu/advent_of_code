"""
with open('input/day9.txt') as fp: prog = { i: int(x) for i, x in enumerate(fp.readline().split(',')) }
pc=0
rb=0
inp = [2]
while True:
  (x, cmd), args = divmod(prog[pc], 100), []
  for (i,rc) in enumerate([[],[1,1,0],[1,1,0],[0],[1],[1,1],[1,1],[1,1,0],[1,1,0],[1]][cmd%99]):
    args += [prog[pc+i+1]]
    if x % 10 == 2: args[-1] += rb
    if x % 10 != 1 and rc != 0: args[-1] = prog.get(args[-1],0)
    x //= 10
  orig_pc = pc
  if cmd == 1: prog[args[2]] = args[0] + args[1] # add
  elif cmd == 2: prog[args[2]] = args[0] * args[1] # multiply
  elif cmd == 3: prog[args[0]] = inp.pop(0) # input
  elif cmd == 4: print(args[0]) # output
  elif cmd == 5 and args[0] != 0: pc = args[1] # branch if true
  elif cmd == 6 and args[0] == 0: pc = args[1] # branch if false
  elif cmd == 7: prog[args[2]] = int(args[0] < args[1]) # test less than
  elif cmd == 8: prog[args[2]] = int(args[0] == args[1]) # test equal
  elif cmd == 9: rb += args[0] # adjust relative base
  elif cmd == 99: break # halt
  if pc == orig_pc: pc += len(args) + 1 #only go to the next instruction if we didn't jump
"""

import fileinput

from collections import defaultdict

def run(program, program_input):
    ip = rb = 0
    mem = defaultdict(int, enumerate(map(int, program.split(','))))
    while True:
        op = mem[ip] % 100
        if op == 99:
            return
        size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
        args = [mem[ip+i] for i in range(1, size)]
        modes = [(mem[ip] // 10 ** i) % 10 for i in range(2, 5)]
        reads = [(mem[x], x, mem[x+rb])[m] for x, m in zip(args, modes)]
        writes = [(x, None, x+rb)[m] for x, m in zip(args, modes)]
        ip += size
        if op == 1:
            mem[writes[2]] = reads[0] + reads[1]
        if op == 2:
            mem[writes[2]] = reads[0] * reads[1]
        if op == 3:
            mem[writes[0]] = program_input.pop(0)
        if op == 4:
            yield reads[0]
        if op == 5 and reads[0]:
            ip = reads[1]
        if op == 6 and not reads[0]:
            ip = reads[1]
        if op == 7:
            mem[writes[2]] = int(reads[0] < reads[1])
        if op == 8:
            mem[writes[2]] = int(reads[0] == reads[1])
        if op == 9:
            rb += reads[0]

program = list(fileinput.input())[0]
print(list(run(program, [1])))
print(list(run(program, [2])))