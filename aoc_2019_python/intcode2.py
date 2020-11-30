
class Intcode:
    def __init__(self, program):
        self.ip = 0
        self.rb = 0
        self.input = []
        self.output = []
        self.finished = False
        with open(program) as file:
            self.memory = [int(val) for val in file.read().split(",")]
            self.memory += [0] * 100000
    
    def run_program(self):
        while self.process():
            pass

    def process(self):
        instruction = self.memory[self.ip] % 100
        
        if instruction == 1: # Add
            parameters = self.get_parameters(3)
            self.memory[parameters[-1]] = parameters[0] + parameters[1]
            self.ip += 4

        elif instruction == 2: # Multiply
            parameters = self.get_parameters(3)
            self.memory[parameters[-1]] = parameters[0] * parameters[1]
            self.ip += 4

        elif instruction == 3: # Input
            if len(self.input) == 0:
                return False
            outPos = self.get_out_pos(1)
            self.memory[outPos] = self.input.pop(0)
            self.ip += 2
        
        elif instruction == 4: # Output
            parameters = self.get_parameters(1)
            self.output.append(parameters[0])
            self.ip += 2

        elif instruction == 5: # Jump if true
            parameters = self.get_parameters(2)
            if parameters[0] != 0:
                self.ip = parameters[1]
            else:
                self.ip += 3

        elif instruction == 6: # Jump if false
            parameters = self.get_parameters(2)
            if parameters[0] == 0:
                self.ip = parameters[1]
            else:
                self.ip += 3

        elif instruction == 7: # Less than
            parameters = self.get_parameters(3)
            if parameters[0] < parameters[1]:
                self.memory[parameters[-1]] = 1
            else:
                self.memory[parameters[-1]] = 0
            self.ip += 4
        
        elif instruction == 8: # Equals
            parameters = self.get_parameters(3)
            if parameters[0] == parameters[1]:
                self.memory[parameters[-1]] = 1
            else:
                self.memory[parameters[-1]] = 0
            self.ip += 4

        elif instruction == 9: # Adjust relative base
            parameters = self.get_parameters(1)
            self.rb += parameters[0]
            self.ip += 2
        
        elif instruction == 99:
            self.finished = True
            return False

        return True

    def get_parameters(self, nr_of_parameters):
        remaining = self.memory[self.ip] // 100
        ret = []
        for i in range(nr_of_parameters):
            value = self.memory[self.ip + 1 + i]
            mode = remaining % 10
            remaining //= 10
            if mode == 0:
                ret.append(self.memory[value])
            elif mode == 1:
                ret.append(value)
            elif mode == 2:
                ret.append(self.memory[self.rb + value])

        ret.append(self.get_out_pos(nr_of_parameters))
        return ret

    def get_out_pos(self, nr_of_parameters):
        value = self.memory[self.ip + nr_of_parameters]
        mode = self.memory[self.ip] // (10 ** (nr_of_parameters + 1))

        if mode == 0:
            return value
        elif mode == 2:
            return self.rb + value
        else:
            return -1
    
    def print_output(self):
        for c in self.output:
            if c < 256:
                print(chr(c), end = '')
            else:
                print(c)
    
    def get_output_string(self):
        return "".join([chr(c) for c in self.output])

    def add_ascii_input(self, command):
        for c in command:
            self.input.append(ord(c))
        self.input.append(10)