import intcode
import time

def main():
    with open("input/day21.txt") as file:
        memory = [int(val) for val in file.read().split(",")]
        memory += [0] * 100000

    program_input = []
    add_function(program_input, "NOT C J")
    add_function(program_input, "AND D J")
    add_function(program_input, "NOT A T")
    add_function(program_input, "OR T J")
    add_function(program_input, "WALK")

    output = []
    intcode.runProgram(memory.copy(), program_input, output)
    for c in output:
        if c < 256:
            #print(chr(c), end = '')
            pass
        else:
            print("part 1:", c, c == 19361332)
    
    
    # ABC[D]EFG[H]I
    program_input = []
    
    # Hole in A or B or C
    add_function(program_input, "NOT A J") 
    add_function(program_input, "NOT B T") 
    add_function(program_input, "OR T J") 
    add_function(program_input, "NOT C T")
    add_function(program_input, "OR T J")

    # Ground in D and (H or (E and I))
    add_function(program_input, "AND D J")
    add_function(program_input, "OR I T")
    add_function(program_input, "AND E T")  
    add_function(program_input, "OR H T")
    add_function(program_input, "AND T J") 
    add_function(program_input, "RUN")

    output = []
    intcode.runProgram(memory, program_input, output)
    for c in output:
        if c < 256:
            #print(chr(c), end = '')
            pass
        else:
            print("part 2:", c, c == 1143351187)

    
def add_function(program_input, function):
    new_line = 10
    for c in function:
        program_input.append(ord(c))
    program_input.append(new_line)

start = time.time()
main()
print(time.time() - start)