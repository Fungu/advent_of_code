import operator
from typing import Callable

def run_simulation(state: dict, cycles: int, directions: list, remain_active_when: Callable, become_active_when: Callable):
    """ 
        Parameters:
        state (dictionary) - Contains all active cells and their neighbors. The key is a position and value is True or False
        cycles (int) - How many cycles to run the simulation 
        directions (list) - All possiple directions. 
        remain_active_when (function) - Function that returns true if an active cell should remain active 
        become_active_when (function) - Function that returns true if an inactive cell should become active
    .
    """
    for pos in list(state.keys()):
        init_neighbors(state, pos, directions)
    for _ in range(cycles):
        next_state = {}
        for pos in state:
            neighbors = count_neighbors(state, pos, directions)
            if state[pos] and remain_active_when(neighbors):
                next_state[pos] = True
                init_neighbors(next_state, pos, directions)
            elif not state[pos] and become_active_when(neighbors):
                next_state[pos] = True
                init_neighbors(next_state, pos, directions)
        state = next_state
    
    return state

def init_neighbors(state, pos, directions):
    for n in directions:
        p = tuple(map(operator.add, n, pos))
        if p not in state:
            state[p] = False

def count_neighbors(state, pos, directions):
    ret = 0
    for n in directions:
        p = tuple(map(operator.add, n, pos))
        if p in state and state[p]:
            ret += 1
    return ret

def count_active(state):
    return len(list(filter(lambda value: value, state.values())))