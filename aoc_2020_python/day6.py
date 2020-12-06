import time
import functools

def main():
    with open("input/day6.txt") as file:
        rawInput = file.read()
    
    print("Part 1:", sum([len(group) for group in [{allAnswers for allAnswers in group.replace("\n", "")} for group in rawInput.split("\n\n")]]))
    print("Part 2:", sum([len(group) for group in [functools.reduce(lambda a, b: list(set(a) & set(b)), group) for group in [[groupAnswers for groupAnswers in group.split("\n")] for group in rawInput.split("\n\n")]]]))

start = time.time()
main()
print("Execution time:", time.time() - start, "ms")