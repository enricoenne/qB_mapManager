import numpy as np
import random
import matplotlib.pyplot as plt

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
    return float("NaN")

size = 5
N = 10000           # how many maps to generate for each p
res = 100           # how many p interval to test
results = np.zeros((res, N))

for k in range(res):
    p = k/res
    for i in range(N):
        m = create_map(size, p)
        results[k, i] = is_solvable(m)
    print(p)

solvable = np.zeros(res)
solvable_mean = np.zeros(res)
solvable_median = np.zeros(res)

for k in range(res):
    current_res = results[k,]
    current_res_solvable = np.invert(np.isnan(current_res))
    solvable[k] = (current_res[current_res_solvable]).sum()
    solvable_mean[k] = np.mean(current_res[current_res_solvable])
    solvable_median[k] = np.median(current_res[current_res_solvable])


solvable = solvable/N



plt.plot(solvable_mean, '#00dd00', solvable_median, '#007700', solvable, '#dd0000')
plt.show()



np.savetxt('data.csv', results, delimiter=',')