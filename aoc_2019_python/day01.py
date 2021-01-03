import aoc

def main(input_lines):
    part1 = 0
    part2 = 0
    for line in input_lines:
        f = get_required_fuel(int(line))
        part1 += f
        while f > 0:
            f = get_required_fuel(f)
            part2 += max(f, 0)
    part2 += part1
    return part1, part2

def get_required_fuel(weight):
    return weight // 3 - 2

aoc.run_lines(main, "day01.txt")