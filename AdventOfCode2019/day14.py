import time
from collections import defaultdict

def nanofactory(reactions, resources):
    while any(r != ORE and resources[r] < 0 for r in resources):
        for target in resources:
            if resources[target] < 0:
                newResources = False
                for reaction in reactions:
                    if target in reaction[1]:
                        nrOfReactions = max(1, int(-resources[target] / reaction[1][target]))
                        for item in reaction[0]:
                            if item not in resources:
                                newResources = True
                            resources[item] -= reaction[0][item] * nrOfReactions
                        for item in reaction[1]:
                            resources[item] += reaction[1][item] * nrOfReactions
                if newResources:
                    break

def main():
    """[
        ({'ORE': 10}, {'A': 10}), 
        ({'ORE': 1}, {'B': 1}), 
        ({'A': 7, 'B': 1}, {'C': 1}), 
        ({'A': 7, 'C': 1}, {'D': 1}), 
        ({'A': 7, 'D': 1}, {'E': 1}), 
        ({'A': 7, 'E': 1}, {'FUEL': 1})
    ]"""
    reactions = []
    with open("input/day14.txt") as file:
        for line in file.readlines():
            reaction = []
            for side in line.split("=>"):
                quantity = {}
                for element in side.split(","):
                    chemical = element.strip().split(" ")
                    quantity[chemical[1]] = int(chemical[0])
                reaction.append(quantity)
            reactions.append(reaction)
    #print(reactions)
    #print("")

    resources = defaultdict(lambda : 0)
    resources[ORE] = TRILLION
    resources[FUEL] = -1
    nanofactory(reactions, resources)
    orePerFuel = TRILLION - resources[ORE]
    print("part 1:", orePerFuel, orePerFuel == 873899)
    
    part2 = 0
    while True:
        resources = defaultdict(lambda : 0)
        resources[ORE] = TRILLION
        resources[FUEL] = -part2
        nanofactory(reactions, resources)
        oreLeft = resources[ORE]
        if oreLeft <= 0:
            part2 -= 1
            break
        else:
            part2 += max(1, int(oreLeft / orePerFuel))

    print("part 2:", part2, part2 == 1893569)

ORE = "ORE"
FUEL = "FUEL"
TRILLION = 1000000000000

start = time.time()
main()
print(time.time() - start)