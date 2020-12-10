import aoc
import scanf

def main(inputLines):
    part1 = 0
    part2 = 0

    for line in inputLines:
        low, high, letter, password = scanf.scanf("%d-%d %c: %s", line)
        if low <= password.count(letter) <= high:
            part1 += 1
        if (password[low - 1] == letter) ^ (password[high - 1] == letter):
            part2 += 1
    
    return part1, part2

aoc.runLines(main, "day02.txt")