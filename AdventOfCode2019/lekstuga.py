import sys
from collections import deque, namedtuple

grid = []
for line in open('input/day18.txt').readlines():
    grid.append(list(line.strip()))
R = len(grid)
C = len(grid[0])
DR = [-1,0,1,0]
DC = [0,1,0,-1]
open_set = deque()
State = namedtuple('State', ['r', 'c', 'keys', 'd'])
all_keys = set()
for r in range(R):
    for c in range(C):
        if grid[r][c]=='@':
            print(r, c, grid[r][c])
            open_set.append(State(r, c, set(), 0))
        if 'a' <= grid[r][c] <= 'z':
            all_keys.add(grid[r][c])
print(len(all_keys), all_keys)

SEEN = set()
while open_set:
    node = open_set.popleft()
    key = (node.r, node.c, tuple(sorted(node.keys)))
    #print(key)
    if key in SEEN:
        continue
    SEEN.add(key)
    if len(SEEN) % 100000 == 0:
        print(len(SEEN))
    if not (0 <= node.r < R and 0 <= node.c < C and grid[node.r][node.c] != '#'):
        continue
    if 'A' <= grid[node.r][node.c] <= 'Z' and grid[node.r][node.c].lower() not in node.keys:
        continue
    newkeys = set(node.keys)
    if 'a' <= grid[node.r][node.c] <= 'z':
        newkeys.add(grid[node.r][node.c])
        if newkeys == all_keys:
            print(node.d)
            sys.exit(0)
    for d in range(4):
        rr, cc = node.r + DR[d], node.c + DC[d]
        open_set.append(State(rr, cc, newkeys, node.d+1))
