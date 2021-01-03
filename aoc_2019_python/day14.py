import aoc
from collections import defaultdict

ORE = "ORE"
FUEL = "FUEL"
TRILLION = 1000000000000

def main(input_lines):
    """
    reactions = [
        [{'ORE': 10}, {'A': 10}], 
        [{'A': 7, 'B': 1}, {'C': 1}], 
        [{'A': 7, 'E': 1}, {'FUEL': 1}]
    ]
    """
    reactions = []
    for line in input_lines:
        reaction = []
        for side in line.split("=>"):
            quantity = {}
            for element in side.split(","):
                chemical = element.strip().split()
                quantity[chemical[1]] = int(chemical[0])
            reaction.append(quantity)
        reactions.append(reaction)

    resources = defaultdict(int)
    resources[ORE] = TRILLION
    resources[FUEL] = -1
    nanofactory(reactions, resources)
    ore_per_fuel = TRILLION - resources[ORE]
    part1 = ore_per_fuel
    
    part2 = 0
    while True:
        resources = defaultdict(int)
        resources[ORE] = TRILLION
        resources[FUEL] = -part2
        nanofactory(reactions, resources)
        ore_remaining = resources[ORE]
        if ore_remaining <= 0:
            part2 -= 1
            break
        else:
            part2 += max(1, int(ore_remaining / ore_per_fuel))

    return part1, part2

def nanofactory(reactions, resources):
    while any(r != ORE and resources[r] < 0 for r in resources):
        for target in resources:
            if resources[target] < 0:
                new_resources = False
                for reaction in reactions:
                    if target in reaction[1]:
                        reaction_count = max(1, int(-resources[target] / reaction[1][target]))
                        for item in reaction[0]:
                            if item not in resources:
                                new_resources = True
                            resources[item] -= reaction[0][item] * reaction_count
                        for item in reaction[1]:
                            resources[item] += reaction[1][item] * reaction_count
                if new_resources:
                    break

aoc.run_lines(main, "day14.txt")