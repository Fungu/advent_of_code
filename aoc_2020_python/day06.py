import aoc
import functools

def main(rawInput):
    part1 = sum([len(group) for group in [{allAnswers for allAnswers in group.replace("\n", "")} for group in rawInput.split("\n\n")]])
    part2 = sum([len(group) for group in [functools.reduce(lambda a, b: list(set(a) & set(b)), group) for group in [[groupAnswers for groupAnswers in group.split("\n")] for group in rawInput.split("\n\n")]]])
    return part1, part2

aoc.runRaw(main, "day06.txt")