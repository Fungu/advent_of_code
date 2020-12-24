import operator

def runSimulation(state, cycles, directions, remainActiveWhen, becomeActiveWhen):
    """ 
        Parameters:
        state (dictionary) - Contains all active cells and their neighbors. 
                             The key is a position and value is True or False
        cycles (int) - How many cycles to run the simulation 
        directions (list) - All possiple directions. 
        remainActiveWhen (function) - Function that returns true if an active cell should remain active 
        becomeActiveWhen (function) - Function that returns true if an inactive cell should become active
    .
    """
    for pos in list(state.keys()):
        initNeighbors(state, pos, directions)
    for _ in range(cycles):
        nextState = {}
        for pos in state:
            neighbors = countNeighbors(state, pos, directions)
            if state[pos] and remainActiveWhen(neighbors):
                nextState[pos] = True
                initNeighbors(nextState, pos, directions)
            elif not state[pos] and becomeActiveWhen(neighbors):
                nextState[pos] = True
                initNeighbors(nextState, pos, directions)
        state = nextState
    
    return state

def initNeighbors(state, pos, directions):
    for n in directions:
        p = tuple(map(operator.add, n, pos))
        if p not in state:
            state[p] = False

def countNeighbors(state, pos, directions):
    ret = 0
    for n in directions:
        p = tuple(map(operator.add, n, pos))
        if p in state and state[p]:
            ret += 1
    return ret

def countActive(state):
    return len(list(filter(lambda value: value, state.values())))