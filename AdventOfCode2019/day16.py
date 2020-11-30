import time
import numpy

def getPatternMatrix(size):
    ret = []
    for i in range(1, size + 1):
        pattern = [0] * i + [1] * i + [0] * i + [-1] * i
        pattern *= size
        ret.append(pattern[1 : size + 1])
    return ret

def main():
    with open("input/day16.txt") as file:
        values = [int(val) for val in file.read()]
    
    patternMatrix = numpy.array(getPatternMatrix(len(values)))
    values = numpy.array(values)
    for _ in range(100):
        values = numpy.matmul(patternMatrix, values)
        values = [abs(r) % 10 for r in values]
    part1 = "".join(map(str, values[:8]))
    print("part 1:", part1, part1 == "27831665")

    with open("input/day16.txt") as file:
        values = file.read()
        values *= 10000
    offset = int(values[:7])
    values = values[offset:]
    values = [int(val) for val in values]
    
    for _ in range(100):
        s = sum(values)
        for i in range(len(values)):
            v = s % 10
            s -= values[i]
            values[i] = v
    part2 = "".join(map(str, values[:8]))
    print("part 2:", part2, part2 == "36265589")


start = time.time()
main()
print(time.time() - start)