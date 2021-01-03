import aoc
import numpy

def get_pattern_matrix(size):
    ret = []
    for i in range(1, size + 1):
        pattern = [0] * i + [1] * i + [0] * i + [-1] * i
        pattern *= size
        ret.append(pattern[1 : size + 1])
    return ret

def main(puzzle_input):
    values = [int(val) for val in puzzle_input]
    
    pattern_matrix = numpy.array(get_pattern_matrix(len(values)))
    values = numpy.array(values)
    for _ in range(100):
        values = numpy.matmul(pattern_matrix, values)
        values = [abs(r) % 10 for r in values]
    part1 = "".join(map(str, values[:8]))

    values = puzzle_input
    values *= 10000
    offset = int(values[:7])
    values = values[offset:]
    values = [int(val) for val in values]
    
    for _ in range(100):
        s = sum(values)
        for i in range(len(values)):
            v = s % 10
            s -= values[i]
            values[i] = v
    part2 = "".join(map(str, values[:8]))

    return part1, part2

aoc.run_raw(main, "day16.txt")