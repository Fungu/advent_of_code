import aoc

def main(lines: list):
    part1 = 0
    part2 = 0

    for line in lines:
        test_value, numbers = line.split(": ")
        test_value = int(test_value)
        numbers = [int(n) for n in numbers.split()]
        if calculate_first(test_value, numbers, 0, 0,  set()):
            part1 += test_value
        if calculate_second(test_value, numbers, 0, 0, set()):
            part2 += test_value
    
    return part1, part2

def calculate_first(test_value, numbers, index, current, dp) -> bool:
    if index == len(numbers):
        return test_value == current
    if current > test_value:
        return False
    
    key = (index, current)
    if key in dp:
        return False
    dp.add(key)
    
    if calculate_first(test_value, numbers, index + 1, current + numbers[index], dp):
        return True
    if calculate_first(test_value, numbers, index + 1, current * numbers[index], dp):
        return True
    
    return False

def calculate_second(test_value, numbers, index, current, dp) -> bool:
    if index == len(numbers):
        return test_value == current
    if current > test_value:
        return False
    
    key = (index, current)
    if key in dp:
        return False
    dp.add(key)
    
    if calculate_second(test_value, numbers, index + 1, current + numbers[index], dp):
        return True
    if calculate_second(test_value, numbers, index + 1, current * numbers[index], dp):
        return True
    if calculate_second(test_value, numbers, index + 1, int(str(current) + str(numbers[index])), dp):
        return True
    
    return False

aoc.run_lines(main, "day07.txt")
