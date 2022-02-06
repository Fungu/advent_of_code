import aoc
import operator

def main(input_lines):
    precedence = { "(": 0, "*": 1, "+": 1 }
    
    part1 = 0
    for line in input_lines:
        part1 += evaluate_postfix(get_postfix(line, precedence))
    
    part2 = 0
    precedence["+"] = 2
    for line in input_lines:
        part2 += evaluate_postfix(get_postfix(line, precedence))
    
    return part1, part2

def get_postfix(line, precedence):
    operator_stack = []
    output = []
    token_list = line.replace("(", " ( ").replace(")", " ) ").split()

    for token in token_list:
        if token.isnumeric():
            output.append(token)
        
        elif token == "(":
            operator_stack.append(token)
        
        elif token == ")":
            while operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            operator_stack.pop()
        
        elif token in "+*":
            while operator_stack and precedence[operator_stack[-1]] >= precedence[token]:
                operator = operator_stack.pop()
                output.append(operator)
            operator_stack.append(token)
    
    while operator_stack:
        output.append(operator_stack.pop())

    return output

def evaluate_postfix(expression):
    operators = { "+": operator.add, "*": operator.mul }
    number_stack = []

    for token in expression:
        if token.isnumeric():
            number_stack.append(int(token))
        
        else:
            result = operators[token](number_stack.pop(), number_stack.pop())
            number_stack.append(result)
    
    return number_stack.pop()

aoc.run_lines(main, "day18.txt")