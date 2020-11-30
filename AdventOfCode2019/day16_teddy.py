import copy
import io
import itertools
import math
import numpy
import re
import sys

base_pattern = [0, 1, 0, -1]

with open("input/day16.txt") as infile:
	raw_input = infile.read().strip()
input = [int(d) for d in raw_input]
data = numpy.array(input)

pattern_array = [[base_pattern[k // i % len(base_pattern)] for k in range(1, len(input) + 1)] for i in range (1, len(input) + 1)]
pattern_matrix = numpy.array(pattern_array)

num_phases = int(sys.argv[2]) if len(sys.argv) > 2 else 100

for i in range(num_phases):
	data = numpy.absolute(pattern_matrix @ data) % 10

print("First 8 digits after {} phases: {}".format(num_phases, "".join([str(d) for d in data[0:8]])))

# Part 2

input *= 10000
offset = int(raw_input[:7])

# The pattern matrix is an upper triangular matrix, so the value of an element is only affected by elements after it.
# Furthermore, the non-zero part of the bottom half of the pattern matrix is all ones.
# I know that my offset leads into the latter half of the input. Let's abuse our knowledge of this to our benefit.
assert(offset > len(input) // 2)

data = numpy.array(input[offset:])

num_phases = int(sys.argv[2]) if len(sys.argv) > 2 else 100

for p in range(num_phases):
	for i in range(-2, -len(data) - 1, -1):
		data[i] += data[i + 1]
		data[i] %= 10

print("First 8 digits at offset {} after {} phases: {}".format(offset, num_phases, "".join([str(d) for d in data[0:8]])))