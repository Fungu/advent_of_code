import aoc

def main(inputLines):
    # This solution is made for entertainment purposes. I would not use this programming style in a serious application.
    bagDict = {outer[0] : [[int(inner.split(" ")[0]), inner[inner.index(" ")+1:]] for inner in outer[1].split(", ")] for outer in [line.replace(".", "").replace("bags", "bag").replace("no ", "0 no ").strip().split(" contain ") for line in inputLines]}

    part1 = len(bagParents(bagDict, "shiny gold bag")) - 1
    part2 = bagContents(bagDict, "shiny gold bag") - 1

    return part1, part2

def bagParents(bagDict, bag):
    ret = {bag}
    for key, value in bagDict.items():
        for potentialBags in value:
            if bag in potentialBags[1]:
                ret.update(bagParents(bagDict, key))
    return ret

def bagContents(bagDict, bag):
    if "no other bag" in bag:
        return 0
    return sum(contents[0] * bagContents(bagDict, contents[1]) for contents in bagDict[bag]) + 1

aoc.runLines(main, "day07.txt")