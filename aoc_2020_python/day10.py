import aoc

def main(inputLines):
    adapters = [int(line) for line in inputLines]
    adapters.append(0)
    adapters = sorted(adapters)
    adapters.append(adapters[-1] + 3)

    differences = [0, 0, 0]
    for i in range(len(adapters) - 1):
        differences[adapters[i + 1] - adapters[i] - 1] += 1
    assert(differences[1] == 0)
    part1 = differences[0] * differences[2]
    
    onesInARow = 0
    part2 = 1
    for i in range(len(adapters) - 1):
        difference = adapters[i + 1] - adapters[i]
        if difference == 1:
            onesInARow += 1
        else:
            if onesInARow <= 1:
                mult = 1
            elif onesInARow == 2:
                mult = 2
            elif onesInARow == 3:
                mult = 4
            elif onesInARow == 4:
                mult = 7
            else:
                assert(False)
            part2 *= mult
            onesInARow = 0

    return part1, part2

aoc.runLines(main, "day10.txt")