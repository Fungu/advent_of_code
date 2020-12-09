import aoc

def main(inputLines):
    xmas = [int(line) for line in inputLines]

    preambleLength = 25
    for i in range(preambleLength + 1, len(xmas)):
        isValid = False
        for a in range(i - preambleLength - 1, i):
            for b in range(a + 1, i):
                if xmas[i] == xmas[a] + xmas[b]:
                    isValid = True
        if not isValid:
            part1 = xmas[i]
            break
    
    contiguousLength = 2
    currentSum = sum(xmas[0 : contiguousLength])
    for i in range(len(xmas)):
        while currentSum < part1:
            currentSum += xmas[i + contiguousLength]
            contiguousLength += 1
        while currentSum > part1 and contiguousLength > 2:
            currentSum -= xmas[i + contiguousLength - 1]
            contiguousLength -= 1
        if currentSum == part1:
            part2 = min(xmas[i : i + contiguousLength]) + max(xmas[i : i + contiguousLength])
            break
        else:
            currentSum -= xmas[i]
            contiguousLength -= 1

    return part1, part2

aoc.runLines(main, "day9")