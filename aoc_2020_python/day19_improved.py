import aoc
import re

def main(inputBlob):
    ruleBlob, messageBlob = inputBlob.split("\n\n")
    rules = {}
    for line in ruleBlob.splitlines():
        name, value = line.strip().split(": ")
        rules[name] = value.replace("\"", "").split()
    messageList = [line.strip() for line in messageBlob.splitlines()]
   
    part1 = sum([match(rules, message) for message in messageList])

    rules["8"] = "42 | 42 8".split()
    rules["11"] = "42 31 | 42 11 31".split()
    part2 = sum([match(rules, message) for message in messageList])

    return part1, part2

def match(inputRules, message, ruleName = "0"):
    currentRules = [inputRules[ruleName]]
    for char in message:
        i = 0
        while i < len(currentRules):
            rule = currentRules[i]
            if len(rule) == 0:
                currentRules.remove(rule)
                continue
            while rule[0].isnumeric():
                innerRule = inputRules[rule[0]]
                if "|" in innerRule:
                    orIndex = innerRule.index("|")
                    newRule = innerRule[orIndex + 1 :] + rule[1:]
                    currentRules.append(newRule)
                    rule = innerRule[: orIndex] + rule[1:]
                    currentRules[i] = rule
                else:
                    rule = innerRule + rule[1:]
                    currentRules[i] = rule
            if rule[0] == char:
                currentRules[i] = rule[1:]
                i += 1
            else:
                currentRules.remove(rule)
    return len(currentRules) != 0 and any([len(r) == 0 for r in currentRules])

aoc.runRaw(main, "day19.txt")