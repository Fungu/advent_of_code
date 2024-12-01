import aoc

def main(input_lines: list):
    left = []
    right = []
    for v in input_lines:
        left.append(int(v.split()[0]))
        right.append(int(v.split()[1]))
    left.sort()
    right.sort()

    part1 = 0
    for i in range(len(input_lines)):
        part1 += abs(left[i] - right[i])
    
    part2 = 0
    for v in left:
        part2 += v * right.count(v)

    return part1, part2

def main_golf(x: list):
    a = sorted([int(v.split()[0]) for v in x])
    b = sorted([int(v.split()[1]) for v in x])

    part1 = sum([abs(a[i] - b[i]) for i in range(len(x))])
    part2 = sum([v * b.count(v) for v in a])

    return part1, part2

aoc.run_lines(main_golf, "day01.txt")
