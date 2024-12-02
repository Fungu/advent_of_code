import aoc

def main(input_lines: list):
    report_list = [[int(a) for a in line.split()] for line in input_lines]
    
    part1 = sum([isSafe(report) for report in report_list])
    
    part2 = sum([any([isSafe(report[0:r] + report[r+1:]) for r in range(len(report))]) for report in report_list])

    return part1, part2

def isSafe(r) -> bool:
    return any(all([abs(r[i] - r[i + 1]) >= 1 and abs(r[i] - r[i + 1]) <= 3 and (r[i] - r[i + 1]) / abs(r[i] - r[i + 1]) == dir for i in range(len(r) - 1)]) for dir in [-1, 1])

aoc.run_lines(main, "day02.txt")
