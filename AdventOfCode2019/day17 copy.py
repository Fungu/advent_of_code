import intcode
import time
import astar
from collections import defaultdict

def main():
    with open("input/day17.txt") as file:
        memory = [int(val) for val in file.read().split(",")]
        memory += [0] * 10000
    

    output = []
    intcode.runProgram(memory.copy(), [], output)
    grid = []
    inner = []
    for c in output:
        if c == 10:
            if len(inner) > 0:
                grid.append(inner)
                inner = []
        else:
            inner.append(chr(c))
        #print(chr(c), end = '')
    dirs = [
        ( 0,-1),
        ( 1, 0),
        ( 0, 1),
        (-1, 0),
    ]
    part1 = 0
    for x in range(1, len(grid[0]) - 1):
        for y in range(1, len(grid) - 1):
            if grid[y][x] == "#" and all(grid[y + yy][x + xx] == "#" for (xx, yy) in dirs):
                part1 += x * y
    print("part 1:", part1, part1 == 3660)

    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] in "^v<>":
                pos = (x, y)
    commands = []
    direction = 0
    distance = 0
    while True:
        next_pos = (pos[0] + dirs[direction][0], pos[1] + dirs[direction][1])
        if not in_bounds(grid, next_pos) or grid[next_pos[1]][next_pos[0]] != "#":
            commands.append(distance)
            distance = 0
            next_direction = direction + 1 if direction < 3 else 0
            next_pos = (pos[0] + dirs[next_direction][0], pos[1] + dirs[next_direction][1])
            if in_bounds(grid, next_pos) and grid[next_pos[1]][next_pos[0]] == "#":
                direction = next_direction
                commands.append("R")
            else:
                next_direction = direction - 1 if direction > 0 else 3
                next_pos = (pos[0] + dirs[next_direction][0], pos[1] + dirs[next_direction][1])
                if in_bounds(grid, next_pos) and grid[next_pos[1]][next_pos[0]] == "#":
                    direction = next_direction
                    commands.append("L")
                else:
                    break
        else:
            pos = next_pos
            distance += 1
    #print(commands[1:])
    
    #for i in range(commands - 1):
        #command += 

    """
    R,6,L,10,R,10,R,10,L,10,L,12,R,10,R,6,L,10,R,10,R,10,L,10,L,12,R,10,R,6,L,10,R,10,R,10,R,6,L,12,L,10,R,6,L,10,R,10,R,10,R,6,L,12,L,10,L,10,L,12,R,10,R,6,L,12,L,10
    """
    """
    ABABACACBC
    A = R6L10R10R10
    B = L10L12R10
    C = R6L12L10
    """

    program_input = []
    add_function(program_input, "A,B,A,B,A,C,A,C,B,C")
    add_function(program_input, "R,6,L,10,R,10,R,10")
    add_function(program_input, "L,10,L,12,R,10")
    add_function(program_input, "R,6,L,12,L,10")
    add_function(program_input, "n")
    memory[0] = 2
    output = []
    ip = 0
    relative_base = 0
    finished = False
    while finished == False:
        ip, finished, relative_base = intcode.runProgram(memory, program_input, output, ip, relative_base)
        #print(ip, finished, relative_base)
        #for c in output:
            #print(chr(c), end = '')
    part2 = output[-1]
    print("part 2:", part2, part2 == 962913)

def in_bounds(grid, pos):
    return pos[0] >= 0 and pos[0] < len(grid[0]) and pos[1] >= 0 and pos[1] < len(grid)

def add_function(program_input, asdf):
    assert len(asdf) <= 20
    for c in asdf:
        program_input.append(ord(c))
    program_input.append(new_line)

new_line = 10
start = time.time()
main()
print(time.time() - start)