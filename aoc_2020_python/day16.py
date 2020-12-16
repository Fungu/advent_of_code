import aoc
import scanf

def main(inputBlob):
    ruleDict = {}
    for line in inputBlob.split("\n\n")[0].strip().splitlines():
        name, a, b, c, d = scanf.scanf("%s:%d-%dor%d-%d", line.replace(" ", ""))
        ruleDict[name] = [a, b, c, d]
    myTicket = [int(a) for a in scanf.scanf("your ticket:\n%s", inputBlob)[0].split(",")]
    nearbyTicketList = [[int(a) for a in b.split(",")] for b in inputBlob.split("nearby tickets:")[1].strip().splitlines()]
    validTicketList = [myTicket]
    
    part1 = 0
    for ticket in nearbyTicketList:
        matchTicket = True
        for value in ticket:
            if not any([match(rule, value) for rule in ruleDict.values()]):
                part1 += value
                matchTicket = False
        if matchTicket:
            validTicketList.append(ticket)

    ticketMatchDict = {}
    for name, rule in ruleDict.items():
        ticketMatchDict[name] = []
        for index in range(len(myTicket)):
            if all([match(rule, ticket[index]) for ticket in validTicketList]):
                ticketMatchDict[name].append(index)
    
    finishedFields = set()
    while len(finishedFields) != len(ticketMatchDict):
        for key, value in ticketMatchDict.items():
            if len(value) == 1 and key not in finishedFields:
                finishedFields.add(key)
                for otherKey, otherValue in ticketMatchDict.items():
                    if key != otherKey and value[0] in otherValue:
                        otherValue.remove(value[0])
    
    part2 = 1
    for key, value in ticketMatchDict.items():
        if key.startswith("departure"):
            part2 *= myTicket[value[0]]

    return part1, part2

def match(rule, value):
    return rule[0] <= value <= rule[1] or rule[2] <= value <= rule[3]

aoc.runRaw(main, "day16.txt")