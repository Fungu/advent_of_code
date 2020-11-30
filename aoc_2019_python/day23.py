from intcode2 import Intcode
import time

def main():
    network = []
    for address in range(50):
        computer = Intcode("input/day23.txt")
        computer.input.append(address)
        computer.run_program()
        network.append(computer)
    
    part1 = False
    previous_nat_y = 0
    while True:
        is_idle = True
        for address in range(50):
            computer = network[address]
            if len(computer.input) == 0:
                computer.input.append(-1)
            else:
                is_idle = False
            
            computer.run_program()
            
            for index in range(0, len(computer.output), 3):
                if computer.output[index] == 255:
                    nat_value = (computer.output[index + 1], computer.output[index + 2])
                    if not part1:
                        part1 = nat_value[1]
                else:
                    target = network[computer.output[index]]
                    target.input.append(computer.output[index + 1])
                    target.input.append(computer.output[index + 2])
            computer.output.clear()
        
        if is_idle:
            if nat_value[1] == previous_nat_y:
                part2 = previous_nat_y
                break
            else:
                previous_nat_y = nat_value[1]
            network[0].input.append(nat_value[0])
            network[0].input.append(nat_value[1])
    
    print("part 1:", part1, part1 == 22074)
    print("part 2:", part2, part2 == 14257)
    
start = time.time()
main()
print(time.time() - start)