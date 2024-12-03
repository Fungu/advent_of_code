import aoc
import re

def main(input: str):
    r = re.compile(r'mul\((?P<a>\d+),(?P<b>\d+)\)')
    part1 = sum([int(m.group("a")) * int(m.group("b")) for m in r.finditer(input)])

    part2 = 0
    do = True
    r = re.compile(r'(?P<do>do\(\))|(?P<dont>don\'t\(\))|(mul\((?P<a>\d+),(?P<b>\d+)\))');
    for m in r.finditer(input):
        if m.group("do"):
            do = True
        elif m.group("dont"):
            do = False
        elif do:
            part2 += int(m.group("a")) * int(m.group("b"))

    return part1, part2

aoc.run_raw(main, "day03.txt")
