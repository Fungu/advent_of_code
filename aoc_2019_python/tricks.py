import math

A = [5,6,7,8,9]
print(A[2:])

for i,x in enumerate(A):
    print(i, x)

print(1j ** 0, 1j ** 1, 1j ** 2, 1j ** 3, 1j ** -1)

print("")
facing = 1j
for i in range(5):
    print(facing)
    facing *= 1j

print("gdc", math.gcd(9, -6))
print("gdc", math.gcd(9, 0))

print("".join(map(str, [3, 6, 2, 6, 5, 5, 8, 9])))

print("".join(["a", "b", "c", "d", "e", "f", "g", "h", "i"][1:5]))

print(["A"] + ["B"])
print(*"A")


two_d_array = [[0 for x in range(10)] for y in range(10)] 
print("a" in "asdf")