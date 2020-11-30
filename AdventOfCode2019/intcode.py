def runProgram(memory, programInput = [], output = [], ip = 0, relativeBase = 0):
    finished = False
    while memory[ip] % 100 != 99:
        ip, finished, relativeBase = process(memory, ip, programInput, output, relativeBase)
        if finished == False:
            break
    return ip, finished, relativeBase

def process(memory, ip, programInput, output, relativeBase = 0):
    instruction = memory[ip] % 100
    
    if instruction == 1: # Add
        parameters = getParameters(memory, ip, relativeBase, 3)
        memory[parameters[-1]] = parameters[0] + parameters[1]
        ip += 4

    elif instruction == 2: # Multiply
        parameters = getParameters(memory, ip, relativeBase, 3)
        memory[parameters[-1]] = parameters[0] * parameters[1]
        ip += 4

    elif instruction == 3: # Input
        if len(programInput) == 0:
            return ip, False, relativeBase
        outPos = getOutPos(memory, ip, relativeBase, 1)
        memory[outPos] = programInput.pop(0)
        ip += 2
    
    elif instruction == 4: # Output
        parameters = getParameters(memory, ip, relativeBase, 1)
        output.append(parameters[0])
        ip += 2

    elif instruction == 5: # Jump if true
        parameters = getParameters(memory, ip, relativeBase, 2)
        if parameters[0] != 0:
            ip = parameters[1]
        else:
            ip += 3

    elif instruction == 6: # Jump if false
        parameters = getParameters(memory, ip, relativeBase, 2)
        if parameters[0] == 0:
            ip = parameters[1]
        else:
            ip += 3

    elif instruction == 7: # Less than
        parameters = getParameters(memory, ip, relativeBase, 3)
        if parameters[0] < parameters[1]:
            memory[parameters[-1]] = 1
        else:
            memory[parameters[-1]] = 0
        ip += 4
    
    elif instruction == 8: # Equals
        parameters = getParameters(memory, ip, relativeBase, 3)
        if parameters[0] == parameters[1]:
            memory[parameters[-1]] = 1
        else:
            memory[parameters[-1]] = 0
        ip += 4

    elif instruction == 9: # Adjust relative base
        parameters = getParameters(memory, ip, relativeBase, 1)
        relativeBase += parameters[0]
        ip += 2

    return ip, True, relativeBase

def getParameters(memory, ip, relativeBase, nrOfParameters):
    remaining = memory[ip] // 100
    ret = []
    for i in range(nrOfParameters):
        value = memory[ip + 1 + i]
        a = remaining % 10
        remaining //= 10
        if a == 0:
            ret.append(memory[value])
        elif a == 1:
            ret.append(value)
        elif a == 2:
            ret.append(memory[relativeBase + value])

    ret.append(getOutPos(memory, ip, relativeBase, nrOfParameters))
    return ret

def getOutPos(memory, ip, relativeBase, nrOfParameters):
    value = memory[ip + nrOfParameters]
    a = memory[ip] // (10 ** (nrOfParameters + 1))

    if a == 0:
        return value
    elif a == 2:
        return relativeBase + value
    else:
        return -1
    
