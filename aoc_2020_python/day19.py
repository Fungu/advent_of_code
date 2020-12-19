import aoc
import re

def main(inputBlob):
    ruleBlob, messageBlob = inputBlob.split("\n\n")
    rules = {}
    for line in ruleBlob.splitlines():
        name, value = line.strip().split(": ")
        rules[name] = value.replace("\"", "").split()
        if "|" in rules[name]:
            rules[name] = ["("] + rules[name] + [")"]
    messageList = [line.strip() for line in messageBlob.splitlines()]

    regex = compileRule(rules, "0")
    part1 = sum([regex.match(message) != None for message in messageList])
    
    rules["8"] = "( 42 | 42 8 )".split()
    rules["11"] = "( 42 31 | 42 11 31 )".split()
    regex = compileRule(rules, "0")
    part2 = sum([regex.match(message) != None for message in messageList])

    return part1, part2

# This solution is too slow for part 2. Figure out a better way to do it.
def compileRule(rules, name, loopLimit = 4):
    finished = False
    rule = rules[name]
    
    loop = 0
    while not finished:
        finished = True
        for i, element in enumerate(rule):
            if element.isnumeric():
                otherRule = rules[element]
                
                # Loop detection
                if element in otherRule:
                    loop += 1
                    # Eliminate the loop after loopLimit iterations
                    if loop > loopLimit:
                        loop = 0
                        orIndex = otherRule.index("|")
                        evilIndex = otherRule.index(element)
                        if orIndex < evilIndex:
                            otherRule = otherRule[:orIndex] + [")"]
                        else:
                            otherRule = ["("] + otherRule[orIndex + 1:]
                rule = rule[:i] + otherRule + rule[i+1:]
                finished = False
                break
    ret = "".join(rule)
    ret = "^" + ret + "$"

    return re.compile(ret)

aoc.runRaw(main, "day19.txt")