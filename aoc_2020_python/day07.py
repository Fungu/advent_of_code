import aoc

def main(input_lines):
    # This solution is made for entertainment purposes. I would not use this programming style in a serious application.
    bag_dict = {outer[0] : [[int(inner.split(" ")[0]), inner[inner.index(" ")+1:]] for inner in outer[1].split(", ")] for outer in [line.replace(".", "").replace("bags", "bag").replace("no ", "0 no ").strip().split(" contain ") for line in input_lines]}

    part1 = len(bag_parents(bag_dict, "shiny gold bag")) - 1
    part2 = bag_contents(bag_dict, "shiny gold bag") - 1

    return part1, part2

def bag_parents(bag_dict, bag):
    ret = {bag}
    for key, value in bag_dict.items():
        for potential_bags in value:
            if bag in potential_bags[1]:
                ret.update(bag_parents(bag_dict, key))
    return ret

def bag_contents(bag_dict, bag):
    if "no other bag" in bag:
        return 0
    return sum(contents[0] * bag_contents(bag_dict, contents[1]) for contents in bag_dict[bag]) + 1

aoc.run_lines(main, "day07.txt")