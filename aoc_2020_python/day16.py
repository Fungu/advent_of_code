import aoc
import scanf

def main(raw_input):
    rule_dict = {}
    for line in raw_input.split("\n\n")[0].strip().splitlines():
        name, a, b, c, d = scanf.scanf("%s:%d-%dor%d-%d", line.replace(" ", ""))
        rule_dict[name] = [a, b, c, d]
    my_ticket = [int(a) for a in scanf.scanf("your ticket:\n%s", raw_input)[0].split(",")]
    nearby_ticket_list = [[int(a) for a in b.split(",")] for b in raw_input.split("nearby tickets:")[1].strip().splitlines()]
    valid_ticket_list = [my_ticket]
    
    part1 = 0
    for ticket in nearby_ticket_list:
        match_ticket = True
        for value in ticket:
            if not any([match(rule, value) for rule in rule_dict.values()]):
                part1 += value
                match_ticket = False
        if match_ticket:
            valid_ticket_list.append(ticket)

    ticket_match_dict = {}
    for name, rule in rule_dict.items():
        ticket_match_dict[name] = []
        for index in range(len(my_ticket)):
            if all([match(rule, ticket[index]) for ticket in valid_ticket_list]):
                ticket_match_dict[name].append(index)
    
    finished_fields = set()
    while len(finished_fields) != len(ticket_match_dict):
        for key, value in ticket_match_dict.items():
            if len(value) == 1 and key not in finished_fields:
                finished_fields.add(key)
                for other_key, other_value in ticket_match_dict.items():
                    if key != other_key and value[0] in other_value:
                        other_value.remove(value[0])
    
    part2 = 1
    for key, value in ticket_match_dict.items():
        if key.startswith("departure"):
            part2 *= my_ticket[value[0]]

    return part1, part2

def match(rule, value):
    return rule[0] <= value <= rule[1] or rule[2] <= value <= rule[3]

aoc.run_raw(main, "day16.txt")