import aoc
import functools

def main(input_lines):
    food_list = []
    for line in input_lines:
        value_list, allergens = line.split(" (contains")
        food_list.append((value_list.split(), allergens.strip().replace(")", "").split(", ")))
    
    equation_system = {}
    for food in food_list:
        value_list, variable_list = food
        for variable in variable_list:
            if variable in equation_system:
                equation_system[variable] = list(set(equation_system[variable]) & set(value_list))
            else:
                equation_system[variable] = value_list

    all_seen_values = functools.reduce(lambda a, b: list(set(a) | set(b)), equation_system.values())
    
    part1 = sum([len(list(filter(lambda value: value not in all_seen_values, value_list))) for value_list, _ in food_list])

    finished = False
    while not finished:
        finished = True
        for variable, value_list in equation_system.items():
            if len(value_list) == 1:
                for other_variable, other_value_list in equation_system.items():
                    if variable != other_variable and value_list[0] in other_value_list:
                        other_value_list.remove(value_list[0])
                        finished = False

    part2 = ",".join([equation_system[a][0] for a in sorted(equation_system.keys())])
    
    return part1, part2

aoc.run_lines(main, "day21.txt")