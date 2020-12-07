import time

def main(rawInput):
    bagDict = {}
    parsedInput = [row.split(" contain ") for row in rawInput]
    for rowPair in parsedInput:
        bagDict[rowPair[0].replace("bags", "bag")] = rowPair[1].replace(".", "").replace("bags", "bag").strip().split(", ")
    part1Set = set()
    openSet = set()
    openSet.add("shiny gold bag")
    while len(openSet) > 0:
        bag = openSet.pop()
        part1Set.add(bag)
        for key, value in bagDict.items():
            for potentialBags in value:
                if bag in potentialBags:
                    openSet.add(key)

    part1 = len(part1Set) - 1
    part2 = sumBags(bagDict, "shiny gold bag") - 1
    return part1, part2

def sumBags(bagDict, bag):
    if "no other bag" in bagDict[bag]:
        return 1
    ret = 1
    for contents in bagDict[bag]:
        for otherBag in contents.split(","):
            amount = int(otherBag.split(" ")[0])
            name = otherBag[otherBag.index(" "):].strip()
            ret += amount * sumBags(bagDict, name)
    return ret

with open("input/day7.txt") as file:
    rawInput = file.readlines()
start = time.time()
part1, part2 = main(rawInput)
print("Execution time:", time.time() - start, "ms")
print("Part 1:", part1)
print("Part 2:", part2)