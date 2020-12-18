import aoc

def main(inputLines):
    part1 = 0
    part2 = 0
    for line in inputLines:
        part1 += evaluate(getExpression(line), False)
        part2 += evaluate(getExpression(line), True)
    
    return part1, part2

def getExpression(line):
    expression = []
    while line:
        value = line[0].strip()
        line = line[1:]
        if value.isnumeric():
            while line and line[0].isnumeric():
                value += line[0]
                line = line[1:]
            expression.append(int(value))
        elif value:
            expression.append(value)
    return expression

def evaluate(expression, additionPriority = False):
    if "(" in expression:
        start = expression.index("(")
        depth = 1
        for i in range(start + 1, len(expression)):
            if expression[i] == "(":
                depth += 1
            elif expression[i] == ")":
                depth -= 1
                if depth == 0:
                    content = evaluate(expression[start + 1 : i], additionPriority)
                    left = expression[: start]
                    right = expression[i + 1 :]
                    return evaluate(left + [content] + right, additionPriority)
    elif len(expression) > 1:
        if not additionPriority:
            index = 1
        else:
            if "+" in expression:
                index = expression.index("+")
            else:
                index = expression.index("*")
        if expression[index] == "+":
            content = expression[index - 1] + expression[index + 1]
        elif expression[index] == "*":
            content = expression[index - 1] * expression[index + 1]
        left = expression[: max(0, index - 1)]
        right = expression[index + 2 :]
        return evaluate(left + [content] + right, additionPriority)
    else:
        return expression[0]

aoc.runLines(main, "day18.txt")