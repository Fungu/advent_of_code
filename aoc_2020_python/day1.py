import time

def main():
    with open("input/day1.txt") as file:
        values = [int(val) for val in file.readlines()]
    
    part1 = [a for a in values if [b for b in values if a + b == 2020]]
    part1 = part1[0] * part1[1]
    print("Part 1: ", part1)

    for a in values:
        for b in values:
            for c in values:
                if a + b + c == 2020:
                    part2 = a * b * c
    print("Part 2: ", part2)

start = time.time()
main()
print("Execution time:", time.time() - start, "ms")