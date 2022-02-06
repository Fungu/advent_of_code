import aoc
import re

def main(input_blob):
    rule_blob, message_blob = input_blob.split("\n\n")
    rules = {}
    for line in rule_blob.splitlines():
        name, value = line.strip().split(": ")
        rules[name] = value.replace("\"", "").split()
        if "|" in rules[name]:
            rules[name] = ["("] + rules[name] + [")"]
    message_list = [line.strip() for line in message_blob.splitlines()]

    regex = compile_rule(rules, "0")
    part1 = sum([regex.match(message) != None for message in message_list])
    
    rules["8"] = "( 42 | 42 8 )".split()
    rules["11"] = "( 42 31 | 42 11 31 )".split()
    regex = compile_rule(rules, "0")
    part2 = sum([regex.match(message) != None for message in message_list])

    return part1, part2

# This solution is too slow for part 2. Figure out a better way to do it.
def compile_rule(rules, name, loop_limit = 4):
    finished = False
    rule = rules[name]
    
    loop = 0
    while not finished:
        finished = True
        for i, element in enumerate(rule):
            if element.isnumeric():
                other_rule = rules[element]
                
                # Loop detection
                if element in other_rule:
                    loop += 1
                    # Eliminate the loop after loop_limit iterations
                    if loop > loop_limit:
                        loop = 0
                        or_index = other_rule.index("|")
                        evil_index = other_rule.index(element)
                        if or_index < evil_index:
                            other_rule = other_rule[:or_index] + [")"]
                        else:
                            other_rule = ["("] + other_rule[or_index + 1:]
                rule = rule[:i] + other_rule + rule[i+1:]
                finished = False
                break
    ret = "".join(rule)
    ret = "^" + ret + "$"

    return re.compile(ret)

aoc.run_raw(main, "day19.txt")