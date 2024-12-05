import time
from typing import Callable

def run_lines(main_function: Callable, day: str):
    with open("input/" + day) as file:
        input = [line.strip() for line in file.readlines()]
    run(main_function, input)

def run_raw(main_function: Callable, day: str):
    with open("input/" + day) as file:
        raw_input = file.read()
    run(main_function, raw_input)

def run(main_function: Callable, raw_input: str):
    start = time.time()
    part1, part2 = main_function(raw_input)
    execution_time = time.time() - start
    execution_time = round(execution_time * 1000)
    print("Execution time:", execution_time, "ms")
    print("Part 1:", part1)
    print("Part 2:", part2)

last_time = time.time()
def time_diff(description):
    global last_time
    t = time.time() - last_time
    t = round(t * 1000)
    print(description, t)
    last_time = time.time()