import aoc
import re

def main(input: str):
    part1 = sum([int(m["a"]) * int(m["b"]) for m in re.finditer(r"mul\((?P<a>\d+),(?P<b>\d+)\)", input)])

    part2 = 0
    do = True
    for m in re.finditer(r"(?P<do>do\(\))|(?P<dont>don't\(\))|(mul\((?P<a>\d+),(?P<b>\d+)\))", input):
        if m["do"]:
            do = True
        elif m["dont"]:
            do = False
        elif do:
            part2 += int(m["a"]) * int(m["b"])

    return part1, part2

aoc.run_raw(main, "day03.txt")
