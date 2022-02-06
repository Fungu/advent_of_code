import aoc
import functools

def main(raw_input):
    # This solution is made for entertainment purposes. I would not use this programming style in a serious application.
    part1 = sum([len(group) for group in [{all_answers for all_answers in group.replace("\n", "")} for group in raw_input.split("\n\n")]])
    part2 = sum([len(group) for group in [functools.reduce(lambda a, b: list(set(a) & set(b)), group) for group in [[group_answers for group_answers in group.split("\n")] for group in raw_input.split("\n\n")]]])
    return part1, part2

aoc.run_raw(main, "day06.txt")