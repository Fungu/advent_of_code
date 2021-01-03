import aoc
from intcode import Intcode
import astar
from collections import defaultdict

def main(puzzle_input):
    #north (1), south (2), west (3), and east (4).
    dir_input = {
        ( 0,-1): 1,
        ( 0, 1): 2,
        (-1, 0): 3,
        ( 1, 0): 4,
    }
    open_stack = list(dir_input.keys())
    area = defaultdict(lambda : -1)
    pos = (0, 0)
    area[pos] = 1
    computer = Intcode(puzzle_input)
    while len(open_stack) > 0:
        pathList = astar.astar(area, pos, open_stack.pop())[1:]

        for path in pathList:
            if path in open_stack:
                open_stack.remove(path)

            direction = dir_input[(path[0] - pos[0], path[1] - pos[1])]
            computer.output.clear()
            computer.input.append(direction)
            computer.run_program()
            
            area[path] = computer.output[0]
            #0: The repair droid hit a wall. Its position has not changed.
            if computer.output[0] == 0:
                pathList.clear()
            #1: The repair droid has moved one step in the requested direction.
            elif computer.output[0] == 1:
                pos = path
            #2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
            elif computer.output[0] == 2:
                oxygen_pos = path
                pos = path

            for test_dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                test_pos = (pos[0] + test_dir[0], pos[1] + test_dir[1])
                if area[test_pos] == -1 and test_pos not in open_stack:
                    open_stack.append(test_pos)

    #printGrid(area, pos)
    part1 = len(astar.astar(area, (0, 0), oxygen_pos)) - 1
    
    next_open_set = set()
    next_open_set.add(oxygen_pos)
    closed_set = set()
    part2 = -1
    while len(next_open_set) > 0 and len(next_open_set) < 2000:
        part2 += 1
        open_set = next_open_set
        next_open_set = set()
        for pos in open_set:
            closed_set.add(pos)
            for test_dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                test_pos = (pos[0] + test_dir[0], pos[1] + test_dir[1])
                if area[(test_pos[0], test_pos[1])] <= 0:
                    continue
                if test_pos in closed_set or test_pos in open_set or test_pos in next_open_set:
                    continue
                next_open_set.add(test_pos)

    return part1, part2

def printGrid(area, pos):
    low_bounds = [0, 0]
    high_bounds = [0, 0]
    for a in area:
        low_bounds[0] = min(low_bounds[0], a[0])
        low_bounds[1] = min(low_bounds[1], a[1])
        high_bounds[0] = max(high_bounds[0], a[0])
        high_bounds[1] = max(high_bounds[1], a[1])
    for y in range(low_bounds[1], high_bounds[1] + 1):
        for x in range(low_bounds[0], high_bounds[0] + 1):
            if pos[0] == x and pos[1] == y:
                print("X", end = '')
            elif x == 0 and y == 0:
                print("S", end = '')
            elif area[(x, y)] == 0:
                print("#", end = '')
            elif area[(x, y)] == 1:
                print(".", end = '')
            elif area[(x, y)] == 2:
                print("O", end = '')
            elif area[(x, y)] == -1:
                print(" ", end = '')
        print("")

aoc.run_raw(main, "day15.txt")