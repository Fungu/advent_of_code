import aoc

def main(x: list):
    a = sorted([int(v.split()[0]) for v in x])
    b = sorted([int(v.split()[1]) for v in x])

    part1 = sum([abs(a[i] - b[i]) for i in range(len(x))])
    part2 = sum([v * b.count(v) for v in a])

    return part1, part2

aoc.run_lines(main, "day01.txt")
