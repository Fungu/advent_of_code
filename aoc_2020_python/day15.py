import aoc

def main(raw_input):
    input_list = [int(a) for a in raw_input.split(",")]
    
    part1 = memory_game(input_list, 2020)
    part2 = memory_game(input_list, 30000000)

    return part1, part2

# Van Eck's sequence
def memory_game(input_list, iterations):
    spoken_numbers = {}
    for i in range(len(input_list)):
        last_number = input_list[i]
        spoken_numbers[last_number] = i
    for i in range(len(input_list), iterations):
        if last_number in spoken_numbers:
            this_number = i - 1 - spoken_numbers[last_number]
        else:
            this_number = 0
        spoken_numbers[last_number] = i - 1
        last_number = this_number
    return last_number

aoc.run_raw(main, "day15.txt")