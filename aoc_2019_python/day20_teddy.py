import io
import itertools
import numpy
import sys
 
def bfs(map, start, goal, walkable_tiles, portals):
    to_search = [(*start, 0, 0)]
    searched = set()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while to_search:
        y, x, layer, d = to_search.pop(0)
        if layer == 0 and (y, x) == goal:
            return d
        searched.add((y, x, layer))
        for dy, dx in dirs:
            ay = y + dy
            ax = x + dx
            dl = 0
            if (ay, ax) in portals:
                ay, ax, dl = portals[(ay, ax)]
            if layer + dl < 0:
                continue
            adjacent = (ay, ax, layer + dl)
            if map[ay, ax] in walkable_tiles and adjacent not in searched and not [True for by, bx, bl, _ in to_search if (by, bx, bl) == adjacent]:
                to_search.append((*adjacent, d + 1))
               
   
 
with open("input/day20.txt") as infile:
    map = numpy.array([list(l) for l in infile.read().splitlines()])
    y_dim, x_dim = map.shape
    outer_offset = 2
    outer_y_dim = y_dim - 2 * outer_offset
    outer_x_dim = x_dim - 2 * outer_offset
    portal_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    empty_space = portal_letters | {' '}
    for co in range(outer_offset, (y_dim + 1) // 2):
        if map[co, co] in empty_space:
            inner_offset = co
            break
   
    portals = {} # NAME: (PORTAL_Y, PORTAL_X, ADJACENT_Y, ADJACENT_X)
    for co in range(outer_offset, y_dim - outer_offset):
        if map[co, 0] in portal_letters:
            portal_name = ''.join(map[co, :outer_offset])
            portals.setdefault(portal_name, []).append((co, outer_offset - 1, co, outer_offset))
        if map[co, -1] in portal_letters:
            portal_name = ''.join(map[co, -outer_offset:])
            portals.setdefault(portal_name, []).append((co, x_dim - outer_offset, co, x_dim - outer_offset - 1))
    for co in range(outer_offset, x_dim - outer_offset):
        if map[0, co] in portal_letters:
            portal_name = ''.join(map[:outer_offset, co])
            portals.setdefault(portal_name, []).append((outer_offset - 1, co, outer_offset, co))
        if map[-1, co] in portal_letters:
            portal_name = ''.join(map[-outer_offset:, co])
            portals.setdefault(portal_name, []).append((y_dim - outer_offset, co, y_dim - outer_offset - 1, co))
    # It doesn't seem to put the inner portals in the corners, where there's a risk of overlap.
    for co in range(inner_offset + outer_offset, y_dim - inner_offset - outer_offset):
        if map[co, inner_offset] in portal_letters:
            portal_name = ''.join(map[co, inner_offset:inner_offset + outer_offset])
            portals.setdefault(portal_name, []).append((co, inner_offset, co, inner_offset - 1))
        if map[co, -inner_offset - 1] in portal_letters:
            portal_name = ''.join(map[co, -outer_offset - inner_offset:-inner_offset])
            portals.setdefault(portal_name, []).append((co, x_dim - inner_offset - 1, co, x_dim - inner_offset))
    for co in range(inner_offset + outer_offset, x_dim - inner_offset - outer_offset):
        if map[inner_offset, co] in portal_letters:
            portal_name = ''.join(map[inner_offset:inner_offset + outer_offset, co])
            portals.setdefault(portal_name, []).append((inner_offset, co, inner_offset - 1, co))
        if map[-inner_offset - 1, co] in portal_letters:
            portal_name = ''.join(map[-outer_offset - inner_offset:-inner_offset, co])
            portals.setdefault(portal_name, []).append((y_dim - inner_offset - 1, co, y_dim - inner_offset, co))
           
    transportation_translation = {} # (PORTAL_Y, PORTAL_X): (DESTINATION_Y, DESTINATION_X, LAYER_DELTA)
    for portal in portals.values():
        if len(portal) == 2:
            (outer_y, outer_x, outer_out_y, outer_out_x), (inner_y, inner_x, inner_out_y, inner_out_x) = portal
            transportation_translation[(outer_y, outer_x)] = (inner_out_y, inner_out_x, -1)
            transportation_translation[(inner_y, inner_x)] = (outer_out_y, outer_out_x, +1)
           
    start = portals["AA"][0][2:]
    goal = portals["ZZ"][0][2:]
    print("Length of shortest path", bfs(map, start, goal, ".", transportation_translation))