import intcode
import time

def main():
    with open("input/day19.txt") as file:
        memory = [int(val) for val in file.read().split(",")]
        memory += [0] * 10000

    part1 = 0
    for y in range(50):
        for x in range(50):
            output = []
            intcode.runProgram(memory.copy(), [x, y], output)
            part1 += output[0]
            #print(output[0], end = "")
        #print("")
    print("part 1:", part1, part1 == 179)


    left = 0
    right = []
    y = 5
    while True:
        for x in range(left, left + 100):    
            output = []
            intcode.runProgram(memory.copy(), [x, y], output)
            if output[0] == 1:
                left = x
                break
        if len(right) == 0:
            right.append(left)
        for x in range(right[-1], right[-1] + 100):    
            output = []
            intcode.runProgram(memory.copy(), [x, y], output)
            if output[0] == 0:
                right.append(x - 1)
                break
        if len(right) > 100:
            if right[-100] - 99 >= left:
                part2 = left * 10000 + y - 99
                break
        #print(y, left, right[-1])
        y += 1
    print("part 2", part2, part2 == 9760485)
    # 9850489 - too high
    # 9830488 - too high
    # 9800486 - too high
    # 9780485 - nope
    # 6670299 - nope
    # 9760484 - nope
    # 9760485 - yep


start = time.time()
main()
print(time.time() - start)