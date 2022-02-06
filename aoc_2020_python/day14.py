import aoc
import scanf

def main(input_lines):
    # Part 1
    memory = {}
    for line in input_lines:
        instruction, value = line.strip().split(" = ")
        if instruction == "mask":
            mask = value
        else:
            address = scanf.scanf("mem[%s]", instruction)[0]
            masked_value = list(bin(int(value))[2:])
            masked_value = ["0"] * (36 - len(masked_value)) + masked_value
            for bi, mask_bit in enumerate(mask):
                if mask_bit == "0":
                    masked_value[bi] = "0"
                elif mask_bit == "1":
                    masked_value[bi] = "1"
            memory[address] = int("".join(masked_value), 2)
    part1 = sum(memory.values())
    
    # Part 2
    memory = {}
    for line in input_lines:
        instruction, value = line.strip().split(" = ")
        if instruction == "mask":
            mask = value
        else:
            address = scanf.scanf("mem[%s]", instruction)[0]
            masked_address = list(bin(int(address))[2:])
            masked_address_list = [["0"] * (36 - len(masked_address)) + masked_address]
            for bi, mask_bit in enumerate(mask):
                if mask_bit == "1":
                    for mi in range(len(masked_address_list)):
                        masked_address_list[mi][bi] = "1"
                elif mask_bit == "X":
                    current_len = len(masked_address_list)
                    for mi in range(current_len):
                        new_address = masked_address_list[mi].copy()
                        new_address[bi] = "1"
                        masked_address_list.append(new_address)
                        masked_address_list[mi][bi] = "0"
            for address in masked_address_list:
                memory[int("".join(address), 2)] = int(value)
    part2 = sum(memory.values())

    return part1, part2

aoc.run_lines(main, "day14.txt")