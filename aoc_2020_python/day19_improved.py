import aoc
import re

def main(raw_input):
    rule_blob, message_blob = raw_input.split("\n\n")
    rules = {}
    for line in rule_blob.splitlines():
        name, value = line.strip().split(": ")
        rules[name] = value.replace("\"", "").split()
    message_list = [line.strip() for line in message_blob.splitlines()]
   
    part1 = sum([match(rules, message) for message in message_list])

    rules["8"] = "42 | 42 8".split()
    rules["11"] = "42 31 | 42 11 31".split()
    part2 = sum([match(rules, message) for message in message_list])

    return part1, part2

def match(input_rules, message, rule_name = "0"):
    current_rules = [input_rules[rule_name]]
    for char in message:
        i = 0
        while i < len(current_rules):
            rule = current_rules[i]
            if len(rule) == 0:
                current_rules.remove(rule)
                continue
            while rule[0].isnumeric():
                inner_rule = input_rules[rule[0]]
                if "|" in inner_rule:
                    or_index = inner_rule.index("|")
                    new_rule = inner_rule[or_index + 1 :] + rule[1:]
                    current_rules.append(new_rule)
                    rule = inner_rule[: or_index] + rule[1:]
                    current_rules[i] = rule
                else:
                    rule = inner_rule + rule[1:]
                    current_rules[i] = rule
            if rule[0] == char:
                current_rules[i] = rule[1:]
                i += 1
            else:
                current_rules.remove(rule)
    return len(current_rules) != 0 and any([len(r) == 0 for r in current_rules])

aoc.run_raw(main, "day19.txt")