import time

def main():
    with open("input/day2.txt") as file:
        lines = file.readlines()
    part1 = 0
    part2 = 0
    
    for line in lines:
        left, password = line.split(":")
        password = password.strip()
        low, right = left.split("-")
        high, letter = right.split(" ")
        count = password.count(letter)
        if count >= int(low) and count <= int(high):
            part1 += 1
        if (password[int(low) - 1] == letter) != (password[int(high) - 1] == letter):
            part2 += 1
    
    print("Part 1: ", part1)
    print("Part 2: ", part2)

start = time.time()
main()
print("Execution time:", time.time() - start, "ms")