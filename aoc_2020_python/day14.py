import aoc
import scanf

def main(inputLines):
    # Part 1
    memory = {}
    for line in inputLines:
        instruction, value = line.strip().split(" = ")
        if instruction == "mask":
            mask = value
        else:
            address = scanf.scanf("mem[%s]", instruction)[0]
            maskedValue = list(bin(int(value))[2:])
            maskedValue = ["0"] * (36 - len(maskedValue)) + maskedValue
            for bi, maskBit in enumerate(mask):
                if maskBit == "0":
                    maskedValue[bi] = "0"
                elif maskBit == "1":
                    maskedValue[bi] = "1"
            memory[address] = int("".join(maskedValue), 2)
    part1 = sum(memory.values())
    
    # Part 2
    memory = {}
    for line in inputLines:
        instruction, value = line.strip().split(" = ")
        if instruction == "mask":
            mask = value
        else:
            address = scanf.scanf("mem[%s]", instruction)[0]
            maskedAddress = list(bin(int(address))[2:])
            maskedAddressList = [["0"] * (36 - len(maskedAddress)) + maskedAddress]
            for bi, maskBit in enumerate(mask):
                if maskBit == "1":
                    for mi in range(len(maskedAddressList)):
                        maskedAddressList[mi][bi] = "1"
                elif maskBit == "X":
                    currentLen = len(maskedAddressList)
                    for mi in range(currentLen):
                        newAddress = maskedAddressList[mi].copy()
                        newAddress[bi] = "1"
                        maskedAddressList.append(newAddress)
                        maskedAddressList[mi][bi] = "0"
            for address in maskedAddressList:
                memory[int("".join(address), 2)] = int(value)
    part2 = sum(memory.values())

    return part1, part2

aoc.runLines(main, "day14.txt")