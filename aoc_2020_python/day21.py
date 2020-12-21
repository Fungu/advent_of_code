import aoc
import functools

def main(inputLines):
    foodList = []
    for line in inputLines:
        valueList, allergens = line.split(" (contains")
        foodList.append((valueList.split(), allergens.strip().replace(")", "").split(", ")))
    
    equationSystem = {}
    for food in foodList:
        valueList, variableList = food
        for variable in variableList:
            if variable in equationSystem:
                equationSystem[variable] = list(set(equationSystem[variable]) & set(valueList))
            else:
                equationSystem[variable] = valueList

    allSeenValues = functools.reduce(lambda a, b: list(set(a) | set(b)), equationSystem.values())
    
    part1 = sum([len(list(filter(lambda value: value not in allSeenValues, valueList))) for valueList, _ in foodList])

    finished = False
    while not finished:
        finished = True
        for variable, valueList in equationSystem.items():
            if len(valueList) == 1:
                for otherVariable, otherValueList in equationSystem.items():
                    if variable != otherVariable and valueList[0] in otherValueList:
                        otherValueList.remove(valueList[0])
                        finished = False

    part2 = ",".join([equationSystem[a][0] for a in sorted(equationSystem.keys())])
    
    return part1, part2

aoc.runLines(main, "day21.txt")