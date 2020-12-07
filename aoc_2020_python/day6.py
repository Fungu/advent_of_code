import time
import functools

def main(rawInput):
    part1 = sum([len(group) for group in [{allAnswers for allAnswers in group.replace("\n", "")} for group in rawInput.split("\n\n")]])
    part2 = sum([len(group) for group in [functools.reduce(lambda a, b: list(set(a) & set(b)), group) for group in [[groupAnswers for groupAnswers in group.split("\n")] for group in rawInput.split("\n\n")]]])
    return part1, part2

with open("input/day6.txt") as file:
    rawInput = file.read()
start = time.time()
part1, part2 = main(rawInput)
print("Execution time:", time.time() - start, "ms")
print("Part 1:", part1)
print("Part 2:", part2)