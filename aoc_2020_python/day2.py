import time
import scanf

def main():
    with open("input/day2.txt") as file:
        lines = file.readlines()
    part1 = 0
    part2 = 0

    for line in lines:
        low, high, letter, password = scanf.scanf("%d-%d %c: %s", line)
        if low <= password.count(letter) <= high:
            part1 += 1
        if (password[low - 1] == letter) ^ (password[high - 1] == letter):
            part2 += 1
    
    print("Part 1:", part1)
    print("Part 2:", part2)

start = time.time()
main()
print("Execution time:", time.time() - start, "ms")