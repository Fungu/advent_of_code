import functools
import aoc

def main(lines: list):
    onRulesSection = True
    updates = []
    for line in lines:
        if len(line) == 0:
            onRulesSection = False
        elif onRulesSection:
            rules.append(line.split("|"))
        else:
            updates.append(line.split(","))

    part1 = 0
    part2 = 0
    for update in updates:
        sortedUpdate = sorted(update, key=functools.cmp_to_key(compare))
        if update == sortedUpdate:
            part1 += int(update[int(len(update) / 2)])
        else:
            part2 += int(sortedUpdate[int(len(sortedUpdate) / 2)])

    return part1, part2

def compare(a, b):
    for rule in rules:
        if rule[0]  == a and rule[1] == b:
            return -1
        if rule[0]  == b and rule[1] == a:
            return 1
    return -1

rules = []
aoc.run_lines(main, "day05.txt")
