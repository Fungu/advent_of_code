import aoc

def main(input_lines: list):
    values = sorted([int(val) for val in input_lines])
    
    combined = {}
    for a in range(len(values)):
        for b in range(a + 1, len(values)):
            combined[values[a] + values[b]] = values[a] * values[b]

    part1 = combined[2020]

    for a in values:
        if 2020 - a in combined:
            part2 = a * combined[2020 - a]
            break

    return part1, part2

aoc.run_lines(main, "day01.txt")