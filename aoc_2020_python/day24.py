import aoc
import gameoflife
import operator
import re

# Cube coordinates (pointy topped)
directions = {
    "se": [0, -1, 1],
    "nw": [0, 1, -1],
    "sw": [-1, 0, 1],
    "ne": [1, 0, -1],
    "e": [1, -1, 0],
    "w": [-1, 1, 0]
}

def main(input_lines):
    state = init_state(input_lines)
    part1 = gameoflife.count_active(state)

    state = gameoflife.run_simulation(
        state, 100, directions.values(), 
        remain_active_when = lambda adjacent_count: 1 <= adjacent_count <= 2,
        become_active_when = lambda adjacent_count: adjacent_count == 2)
    part2 = gameoflife.count_active(state)

    return part1, part2

def init_state(input_lines):
    state = {}
    prog = re.compile("se|nw|sw|ne|e|w")
    for line in input_lines:
        position = (0, 0, 0)
        for dir_string in prog.findall(line):
            position = tuple(map(operator.add, position, directions[dir_string]))
        state[position] = not (position in state and state[position])
    return state

aoc.run_lines(main, "day24.txt")