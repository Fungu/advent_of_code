def calculateHash(decks):
    ret = 0
    mult = len(decks[0])
    for i in range(len(decks[0])):
        ret += decks[0][i] * mult
        mult -= 1
    ret2 = 0
    mult = len(decks[1])
    for i in range(len(decks[1])):
        ret2 += decks[1][i] * mult
        mult -= 1
    
    return (ret, ret2)

b = [[1, 2], [3, 4, 5, 6]]

prev = set()
a = [[1, 2, 3], [4, 5, 6]]
aa = str(a)
prev.add(aa)
a[0].append(a[0][0])
a[0].append(a[1][0])
a[0] = a[0][1:]
a[1] = a[1][1:]
bb = str(a)
print(bb in prev)
prev.add(bb)
print(prev)
a[0] = a[0][1:]
a[1] = a[1][1:]
bb = str(a)
print(bb in prev)

prev = set()
aa = calculateHash(a)
prev.add(aa)
a[0].append(a[0][0])
a[0].append(a[1][0])
a[0] = a[0][1:]
a[1] = a[1][1:]
bb = calculateHash(a)
print(bb in prev)
prev.add(bb)
print(prev)