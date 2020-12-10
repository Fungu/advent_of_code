import aoc

def main(inputLines):
    values = [int(val) for val in inputLines]
    
    part1 = [a for a in values if [b for b in values if a + b == 2020]]
    part1 = part1[0] * part1[1]

    for a in values:
        for b in values:
            for c in values:
                if a + b + c == 2020:
                    part2 = a * b * c
    
    return part1, part2

aoc.runLines(main, "day01.txt")