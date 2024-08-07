import numpy as np
import random
import matplotlib.pyplot as plt
import math

def read_map(path):
    file = open(path, 'r')
    lines = file.readlines()

    return None

def text_to_map(text):
    lines = text.splitlines()

    n = int(math.sqrt(len(lines)))
    print(n)

    m = np.zeros((n, n, n))

    for x in range(n):
        for y in range(n):
            for z in range(n):
                if lines[n * x + y][z] == 'w':
                    m[x, y, z] = 1
                elif lines[n * x + y][z] == 'o':
                    m[x, y, z] = 2
    return m

def write_map(m, path, id):
    n = m.shape[0]
    file_name = path + str(n) + "-" + str(id) + ".txt"

    sol = is_solvable(m)

    m = m.astype(int)

    with open(file_name, "w") as file:
        for slice_2d in m:
            for row in slice_2d:
                row_string = ''.join(map(str, row))
                file.write(row_string + '\n')

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

def multiple_map_analysis(s = 5, N = 10000, res = 100):
    size = 5
    # how many maps to generate for each p
    # how many p interval to test
    results = np.zeros((res, N))

    for k in range(res):
        p = k / res
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

    solvable = solvable / N

    plt.plot(solvable_mean, '#00dd00', solvable_median, '#007700', solvable, '#dd0000')
    plt.show()

    np.savetxt('data.csv', results, delimiter=',')

'''m = create_map(4, 0.25)
print(is_solvable(m))

write_map(m, "maps/", 1)'''

m = text_to_map(""" w  
w   
    
ww o
  w 
www 
 w  
 w w
  w 
 www
  ww
 ww 
 www
   w
w w 
w  w
""")

write_map(m, 'maps/', 'old-4')