import aoc

def main(data: str):
    part1 = 0
    part2 = 0
    
    stones = [int(d) for d in data.strip().split(" ")]
    
    dp1 = {}
    dp2 = {}
    for stone in stones:
        part1 += simulate(stone, 0, 25, dp1)
        part2 += simulate(stone, 0, 75, dp2)

    return part1, part2

def simulate(stone: int, iteration: int, target_iterations: int, dp: map):
    if iteration == target_iterations:
        return 1
    if (stone, iteration) in dp:
        return dp[(stone, iteration)]

    #If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if stone == 0:
        ret = simulate(1, iteration + 1, target_iterations, dp)
    
    #If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. 
    # The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. 
    # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        left = simulate(int(s[0 : int(len(s) / 2)]), iteration + 1, target_iterations, dp)
        right = simulate(int(s[int(len(s) / 2) : len(s)]), iteration + 1, target_iterations, dp)
        ret = left + right

    #If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    else:
        ret = simulate(stone * 2024, iteration + 1, target_iterations, dp)
    
    dp[(stone, iteration)] = ret
    return ret

aoc.run_raw(main, "day11.txt")
