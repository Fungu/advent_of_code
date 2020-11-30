import sys
import datetime

with open("input/day4.txt") as file:
    pw_range = [int(x) for x in file.read().split('-')]
start = datetime.datetime.now()

i = pw_range[0]
num_possible_matches = 0

while i <= pw_range[1]:
	validated = False
	while not validated:
		doublet = -1
		multiplet = -1
		prev_digit = -1
		validated = True
		for x in range(6):
			demodulator = 10 ** (5 - x)
			duplicator = 111111 // 10 ** (x)
			digit = (i // demodulator) % 10
			if digit == prev_digit and digit != multiplet:
				if doublet < 0:
					doublet = digit
				elif doublet == digit:
					doublet = -2
					multiplet = digit
			if digit < prev_digit:
				i = i - (digit * demodulator + i % demodulator) + prev_digit * duplicator
				validated = False
				break
			prev_digit = digit
		else:
			if doublet == -1:
				i += 10 - digit
				validated = False
			elif doublet == -2:
				i += 1
				validated = False
	if (i <= pw_range[1]):
		num_possible_matches += 1
		i += 1
	
print(num_possible_matches)
print(datetime.datetime.now() - start)