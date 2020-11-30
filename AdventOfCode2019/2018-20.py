import collections

distances = collections.defaultdict(lambda:1e9)
position = distances[0] = 0
stack = []
regex = open('input/2018-20.txt').read()
for character in regex[1 : -1]:
    if '(' == character:
        stack.append(position)
    elif ')' == character:
        position = stack.pop()
    elif '|' == character:
        position = stack[-1]
    else:
        lastPosition = position
        position += 1j ** 'ESWN'.index(character)
        distances[position] = min(distances[position], distances[lastPosition] + 1)

part1 = max(distances.values())
part2 = sum(x >= 1000 for x in distances.values())
print("part 1: ", part1, part1 == 3930)
print("part 2: ", part2, part2 == 8240)