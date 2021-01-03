import aoc

def main(puzzle_input):
    low, high = puzzle_input.split("-")

    numbers = [int(val) for val in low]
    for i in range(1, 6):
        if numbers[i - 1] > numbers[i]:
            for j in range(i, 6):
                numbers[j] = numbers[j - 1]
    
    maxLimit = int(high)
    part1 = 0
    part2 = 0
    password = int(''.join([str(n) for n in numbers]))
    while password <= maxLimit:
        if has_same(password, False):
            part1 += 1
        if has_same(password, True):
            part2 += 1
        
        index = 5
        numbers[index] += 1
        while numbers[index] == 10:
            numbers[index] = 0
            numbers[index - 1] += 1
            index -= 1
        for i in range(index, 6):
            numbers[i] = max(numbers[i], numbers[i - 1])
        password = int(''.join([str(n) for n in numbers]))
    
    return part1, part2

def has_same(password, part2 = False):
    passwordString = str(password)
    for i in range(5):
        if passwordString[i] == passwordString[i + 1]:
            if part2 == False:
                return True
            elif (i == 0 or passwordString[i] != passwordString[i - 1]) and (i == 4 or passwordString[i] != passwordString[i + 2]):
                return True
    return False

aoc.run_raw(main, "day04.txt")
