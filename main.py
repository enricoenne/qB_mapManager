import numpy as np
import random

def read_map(path):
    return None
def write_map(path):
    return None

def create_map(n, p):
    # player start at 0,0,0
    # empty space value is 0

    # target position is random
    # target value = 2

    # p probability of a wall
    # wall value is 1

    m = np.zeros((n, n, n))
    target = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))

    m[target] = 2

    for idx, value in np.ndenumerate(m):
        if idx != (0,0,0) and m[idx] != 2:
            if random.random() < p:
                m[idx] = 1

    return m

def is_valid_pos(m, pos):
    # if index is a wall or out of bound it's an oopsie
    try:
        if m[pos] != 1 and min(pos) >= 0:
            return True
        else:
            return False
    except IndexError:
        return False

def single_move(m, pos, dir):
    pos = np.array(pos)
    dir = np.array(dir)

    new_pos = tuple((pos + dir).tolist())

    while is_valid_pos(m, new_pos):
        # print(pos, new_pos)
        pos = pos + dir
        new_pos = tuple((pos + dir).tolist())

    return tuple(pos.tolist())

# is the map solvable and how many steps it takes
def is_solvable(m):
    # positions to explore
    tree = list()
    # starting at (0,0,0)
    tree.append(((0, 0, 0), 0))

    # position already visited
    visited_pos = {(0, 0, 0): 1}

    # all possible directions to explore
    all_dir = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    while len(tree) != 0:
        cur_pos, depth = tree.pop(0)
        for d in all_dir:
            new_pos = single_move(m, cur_pos, d)
            if m[new_pos] == 2:
                return depth+1
            if new_pos not in visited_pos:
                visited_pos[new_pos] = 1
                tree.append((new_pos, depth+1))
    return -1


m = create_map(2,1)

print(is_solvable(m))