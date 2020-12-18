import aoc
import operator

def main(inputLines):
    precedence = { "(": 0, "*": 1, "+": 1 }
    
    part1 = 0
    for line in inputLines:
        part1 += evaluatePostfix(getPostfix(line, precedence))
    
    part2 = 0
    precedence["+"] = 2
    for line in inputLines:
        part2 += evaluatePostfix(getPostfix(line, precedence))
    
    return part1, part2

def getPostfix(line, precedence):
    operatorStack = []
    output = []
    tokenList = line.replace("(", " ( ").replace(")", " ) ").split()

    for token in tokenList:
        if token.isnumeric():
            output.append(token)
        
        elif token == "(":
            operatorStack.append(token)
        
        elif token == ")":
            while operatorStack[-1] != "(":
                output.append(operatorStack.pop())
            operatorStack.pop()
        
        elif token in "+*":
            while operatorStack and precedence[operatorStack[-1]] >= precedence[token]:
                operator = operatorStack.pop()
                output.append(operator)
            operatorStack.append(token)
    
    while operatorStack:
        output.append(operatorStack.pop())

    return output

def evaluatePostfix(expression):
    operators = { "+": operator.add, "*": operator.mul }
    numberStack = []

    for token in expression:
        if token.isnumeric():
            numberStack.append(int(token))
        
        else:
            result = operators[token](numberStack.pop(), numberStack.pop())
            numberStack.append(result)
    
    return numberStack.pop()

aoc.runLines(main, "day18.txt")