import aoc
from intcode import Intcode

def main(puzzle_input):
    computer = Intcode(puzzle_input)
    computer.run_program()

    grid = []
    inner = []
    for c in computer.output:
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
            if grid[y][x] == "#" and all(grid[y + yy][x + xx] == "#" for (xx, yy) in [(0, -1),(1, 0),(0, 1),(-1, 0)]):
                part1 += x * y


    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] in "^v<>":
                pos = x + y * 1j
                direction = {"^": -1j, "v": 1j, "<": -1, ">": 1}[grid[y][x]]
                break
    
    commands = find_commands(pos, direction, grid)
    functions = find_functions(commands, [])
    main_routine = create_main_routine(commands, functions)

    program_input = []
    add_function(program_input, main_routine)
    for function in functions:
        add_function(program_input, ",".join(map(str, function)))
    add_function(program_input, "n")
    #add_function(program_input, "A,B,A,B,A,C,A,C,B,C")
    #add_function(program_input, "R,6,L,10,R,10,R,10")
    #add_function(program_input, "L,10,L,12,R,10")
    #add_function(program_input, "R,6,L,12,L,10")
    #add_function(program_input, "n")

    computer = Intcode(puzzle_input)
    computer.memory[0] = 2
    computer.input = program_input
    computer.run_program()
    part2 = computer.output[-1]

    return part1, part2

def find_commands(pos, direction, grid):
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
    return commands

def find_functions(commands, functions):
    if len(functions) == 3:
        if len(commands) == 0:
            return functions
        else:
            return False
    commands_string = ",".join(map(str, commands))
    max_size = 20
    function = []
    matches = 0
    for i in range(0, len(commands)-1, 2):
        next_function = function.copy()
        next_function.append(commands[i])
        next_function.append(commands[i+1])
        next_function_string = ",".join(map(str, next_function))
        next_matches = commands_string.count(next_function_string)
        if next_matches < matches or len(next_function_string) > max_size:
            sub_commands_string = commands_string.replace(",".join(map(str, function)), "")
            sub_commands = [c for c in sub_commands_string.split(",") if c.strip()]
            sub_functions = functions.copy()
            sub_functions.append(function.copy())
            possible_solution = find_functions(sub_commands, sub_functions)
            if possible_solution:
                return possible_solution
        if len(next_function_string) > max_size:
            return False
        matches = next_matches
        function = next_function
    functions.append(function)
    return functions

def create_main_routine(commands, functions):
    abc = ["A", "B", "C"]
    commands_string = ",".join(map(str, commands))
    for i, function in enumerate(functions):
        function_string = ",".join(map(str, function))
        commands_string = commands_string.replace(function_string, abc[i])
    return commands_string

def in_bounds(grid, pos):
    return pos.real >= 0 and pos.real < len(grid[0]) and pos.imag >= 0 and pos.imag < len(grid)

def add_function(program_input, function):
    assert len(function) <= 20
    new_line = 10
    for c in function:
        program_input.append(ord(c))
    program_input.append(new_line)

aoc.run_raw(main, "day17.txt")