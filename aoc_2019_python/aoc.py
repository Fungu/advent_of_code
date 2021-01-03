import time

def run_lines(main_function, day):
    with open("input/" + day) as file:
        main_input = file.readlines()
    run(main_function, main_input)

def run_raw(main_function, day):
    with open("input/" + day) as file:
        main_input = file.read()
    run(main_function, main_input)

def run(main_function, main_input):
    start = time.time()
    part1, part2 = main_function(main_input)
    execution_time = time.time() - start
    execution_time = round(execution_time * 1000)
    print("Execution time:", execution_time, "ms")
    print("Part 1:", part1)
    print("Part 2:", part2)

prev_time = time.time()
def time_diff(description):
    global prev_time
    t = time.time() - prev_time
    t = round(t * 1000)
    print(description, t)
    prev_time = time.time()