import intcode

def main():
    with open("input/day5.txt") as file:
        memory = [int(val) for val in file.read().split(",")]

    output = []
    intcode.runProgram(memory.copy(), [1], output)
    print("part 1: ", output[-1], output[-1] == 13294380)

    output = []
    intcode.runProgram(memory.copy(), [5], output)
    print("part 2: ", output[0], output[0] == 11460760)
 
main()