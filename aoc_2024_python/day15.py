import aoc

def main(lines: list):
    part1 = 0
    part2 = 0
    
    warehouse_segment = True
    movements = ""
    pos = []
    warehouse = []
    boxes = []
    big_pos = []
    big_warehouse = []
    big_boxes = []
    for y, line in enumerate(lines):
        if line == "":
            warehouse_segment = False
            continue
        if warehouse_segment:
            for x, c in enumerate(line):
                if c == "@":
                    pos = [x, y]
                    big_pos = [x * 2, y]
                if c == "O":
                    boxes.append([x, y])
                    big_boxes.append([x * 2, y])
            l = line.replace("@", ".").replace("O", ".")
            warehouse.append(l)
            l = l.replace("#", "##").replace(".", "..")
            big_warehouse.append(l)
        else:
            movements += line.strip()

    directions = {
        "<": [-1, 0],
        ">": [1, 0],
        "^": [0, -1],
        "v": [0, 1],
    }
    for movement in movements:
        dir = directions[movement]
        test_pos = pos.copy()
        while True:
            test_pos[0] += dir[0]
            test_pos[1] += dir[1]
            if test_pos in boxes:
                continue
            if warehouse[test_pos[1]][test_pos[0]] == ".":
                pos[0] += dir[0]
                pos[1] += dir[1]
                if pos in boxes:
                    i = boxes.index(pos)
                    boxes[i][0] = test_pos[0]
                    boxes[i][1] = test_pos[1]
            break
    part1 = sum([box[0] + 100 * box[1] for box in boxes])

    for movement in movements:
        if False:
            for y in range(len(big_warehouse)):
                for x in range(len(big_warehouse[0])):
                    if [x, y] in big_boxes:
                        print("[", end='')
                    elif [x - 1, y] in big_boxes:
                        print("]", end='')
                    elif big_pos == [x, y]:
                        print("@", end='')
                    else:
                        print(big_warehouse[y][x], end='')
                print()
            input()
        
        dir = directions[movement]
        affected_boxes = set()
        checked_positions = set()
        if test_move(big_warehouse, big_boxes, big_pos, dir, affected_boxes, checked_positions):
            big_pos = [big_pos[0] + dir[0], big_pos[1] + dir[1]]
            for i in affected_boxes:
                big_boxes[i][0] += dir[0]
                big_boxes[i][1] += dir[1]
        
    part2 = sum([box[0] + 100 * box[1] for box in big_boxes])
    
    return part1, part2

def test_move(warehouse, boxes, pos, dir, affected_boxes: set, checked_positions: set):
    p = (pos[0], pos[1])
    if p in checked_positions:
        return True
    checked_positions.add(p)
    next_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    
    # Check if we hit the left side of a box
    if next_pos in boxes:
        ret = test_move(warehouse, boxes, next_pos, dir, affected_boxes, checked_positions) and test_move(warehouse, boxes, [next_pos[0] + 1, next_pos[1]], dir, affected_boxes, checked_positions)
        if ret and pos in boxes:
            affected_boxes.add(boxes.index(pos))
        return ret
    
    # Check if we hit the right side of a box
    next_pos_right = [next_pos[0] - 1, next_pos[1]]
    if next_pos_right in boxes:
        ret = test_move(warehouse, boxes, next_pos_right, dir, affected_boxes, checked_positions) and test_move(warehouse, boxes, next_pos, dir, affected_boxes, checked_positions)
        if ret and pos in boxes:
            affected_boxes.add(boxes.index(pos))
        return ret
    
    if warehouse[next_pos[1]][next_pos[0]] == ".":
        if pos in boxes:
            affected_boxes.add(boxes.index(pos))
        return True
    else:
        return False

aoc.run_lines(main, "day15.txt")
