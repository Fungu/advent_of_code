import intcode
import time

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
    
    part1 = 0
    for x in range(1, len(grid[0]) - 1):
        for y in range(1, len(grid) - 1):
            if grid[y][x] == "#" and all(grid[y + yy][x + xx] == "#" for (xx, yy) in [( 0,-1),( 1, 0),( 0, 1),(-1, 0)]):
                part1 += x * y
    print("part 1:", part1, part1 == 3660)


    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] in "^v<>":
                pos = x + y * 1j
                direction = {"^": -1j, "v": 1j, "<": -1, ">": 1}[grid[y][x]]
    commands = []
    distance = 0
    while True:
        next_pos = pos + direction
        if not in_bounds(grid, next_pos) or grid[int(next_pos.imag)][int(next_pos.real)] != "#":
            commands.append(distance)
            distance = 0

            finished = True
            for value, next_direction in {"R": direction * 1j, "L": direction * -1j}.items():
                next_pos = pos + next_direction
                if in_bounds(grid, next_pos) and grid[int(next_pos.imag)][int(next_pos.real)] == "#":
                    direction = next_direction
                    commands.append(value)
                    finished = False
            if finished:
                break
        else:
            pos = next_pos
            distance += 1
    commands = commands[1:]
    #print(commands)

    program_input = []
    add_function(program_input, "A,B,A,B,A,C,A,C,B,C")
    add_function(program_input, "R,6,L,10,R,10,R,10")
    add_function(program_input, "L,10,L,12,R,10")
    add_function(program_input, "R,6,L,12,L,10")
    add_function(program_input, "n")
    memory[0] = 2
    output = []
    intcode.runProgram(memory, program_input, output)
    #for c in output:
        #print(chr(c), end = '')
    part2 = output[-1]
    print("part 2:", part2, part2 == 962913)

def in_bounds(grid, pos):
    return pos.real >= 0 and pos.real < len(grid[0]) and pos.imag >= 0 and pos.imag < len(grid)

def add_function(program_input, function):
    assert len(function) <= 20
    new_line = 10
    for c in function:
        program_input.append(ord(c))
    program_input.append(new_line)

start = time.time()
main()
print(time.time() - start)