import aoc

def main(input_lines):
    part1 = 0
    part2 = 0
    for line in input_lines:
        part1 += evaluate(get_expression(line), False)
        part2 += evaluate(get_expression(line), True)
    
    return part1, part2

def get_expression(line):
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

def evaluate(expression, addition_priority = False):
    if "(" in expression:
        start = expression.index("(")
        depth = 1
        for i in range(start + 1, len(expression)):
            if expression[i] == "(":
                depth += 1
            elif expression[i] == ")":
                depth -= 1
                if depth == 0:
                    content = evaluate(expression[start + 1 : i], addition_priority)
                    left = expression[: start]
                    right = expression[i + 1 :]
                    return evaluate(left + [content] + right, addition_priority)
    elif len(expression) > 1:
        if not addition_priority:
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
        return evaluate(left + [content] + right, addition_priority)
    else:
        return expression[0]

aoc.run_lines(main, "day18.txt")