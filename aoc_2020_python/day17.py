import aoc
import gameoflife
import itertools

def main(input_lines):
    neighbors3d, neighbors4d = get_neighbor_types()
    state = init_state(input_lines)
    remain_active_when = lambda adjacent_count: adjacent_count in [2, 3]
    become_active_when = lambda adjacent_count: adjacent_count == 3

    state1 = gameoflife.run_simulation(state, 6, neighbors3d, remain_active_when, become_active_when)
    part1 = gameoflife.count_active(state1)

    state2 = gameoflife.run_simulation(state, 6, neighbors4d, remain_active_when, become_active_when)
    part2 = gameoflife.count_active(state2)

    return part1, part2

def get_neighbor_types():
    directions = [-1, 0, 1]
    neighbors3d = list(itertools.product(directions, directions, directions, [0]))
    neighbors4d = list(itertools.product(directions, directions, directions, directions))
    neighbors3d.remove((0, 0, 0, 0))
    neighbors4d.remove((0, 0, 0, 0))
    return neighbors3d, neighbors4d

def init_state(input_lines):
    state = {}
    for row, line in enumerate(input_lines):
        for col, char in enumerate(line):
            state[(row, col, 0, 0)] = char == "#"
    return state

aoc.run_lines(main, "day17.txt")