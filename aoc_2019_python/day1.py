import math

def main():
    file = open("input/day1.txt")

    result = 0
    result2 = 0
    for line in file.readlines():
        f = get_required_fuel(int(line))
        result += f
        while f > 0:
            f = get_required_fuel(f)
            result2 += max(f, 0)
            
    print("part 1: " + str(result))
    print("part 2: " + str(result + result2))

def get_required_fuel(weight):
    return math.floor(weight / 3) - 2

main()