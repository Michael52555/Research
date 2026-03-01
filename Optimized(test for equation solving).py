from itertools import product

def build_support_masks(mapping, stindic, indic, outdic, pos, size, total):
    # variable id for each mapped entry
    var_id = { (mapping[t][0]-1, mapping[t][1]-1): t for t in range(total) }

    # precompute candidate lists once
    cand = [[None]*size for _ in range(size)]
    for i in range(size):
        k = stindic[i]
        for j in range(size):
            if k == -1:
                cand[i][j] = (-1, [])
                continue
            res = []
            for l in outdic[k]:
                if l != i:
                    res.append((l, j))
            for m in indic[j]:
                res.append((k, m))
            cand[i][j] = (k, res)

    support = [[0]*size for _ in range(size)]
    state   = [[0]*size for _ in range(size)]  # 0=unseen, 1=visiting, 2=done

    def dfs(i, j):
        if state[i][j] == 2:
            return support[i][j]
        if state[i][j] == 1:
            raise ValueError(f"cycle at {(i,j)}")

        state[i][j] = 1

        # forced-solved region (your pos rule)
        if pos[j+1] >= pos[i+1]:
            support[i][j] = 0
            state[i][j] = 2
            return 0

        # mapped variable cell
        if (i, j) in var_id:
            support[i][j] = 1 << var_id[(i, j)]
            state[i][j] = 2
            return support[i][j]

        k, deps = cand[i][j]
        if k == -1:
            # stays whatever constant you set; in your code it's 0 unless mapped
            support[i][j] = 0
            state[i][j] = 2
            return 0

        if not deps:
            support[i][j] = 0
            state[i][j] = 2
            return 0

        mask = 0
        for (u, v) in deps:
            mask |= dfs(u, v)

        support[i][j] = mask
        state[i][j] = 2
        return mask

    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                dfs(i, j)

    return support

def gf2_rank(masks):
    pivots = {}
    for x in masks:
        v = x
        while v:
            b = v.bit_length() - 1
            if b in pivots:
                v ^= pivots[b]
            else:
                pivots[b] = v
                break
    return len(pivots)

def fast_experiment(mapping, arrows, starrows, pos, size, total, mu):
    stindic = {a: -1 for a in range(size)}
    stoutdic = {a: -1 for a in range(size)}
    indic = {a: [] for a in range(size)}
    outdic = {a: [] for a in range(size)}

    for (a,b) in arrows:
        indic[b-1].append(a-1)
        outdic[a-1].append(b-1)

    for (a,b) in starrows:
        stindic[b-1] = a-1
        stoutdic[a-1] = b-1

    support = build_support_masks(mapping, stindic, indic, outdic, pos, size, total)

    U = set(range(size))
    forbidden = []
    for i in mu:
        for j in U - mu:
            if support[i][j]:
                forbidden.append((i,j,support[i][j]))
    print(len(forbidden))
    print(forbidden[:20])

    # Only check forbidden block cells that could ever become nonzero
    forbidden = []
    for i in mu:
        for j in set(range(size))-mu:
            m = support[i][j]
            if m != 0:
                forbidden.append(m)
    # used = 0
    # for m in forbidden:
    #     used |= m
    # unused = total - used.bit_count()$
    # print("len(forbidden) =", len(forbidden),
    #     "rank =", gf2_rank(forbidden),
    #     "unused_vars =", unused)

    r = gf2_rank(forbidden)
    return 1 << (total - r)

#



# mapping = [(7,1), (7,2), (7,5), (7,3), (7,6), (7,7), (6,1), (6,2), (6,5), (6,3), (6,6), (6,7), (8,1), (8,2), (8,5), (8,3), (8,6), (8,7), (8, 4), (8,8)]
# arrows = [(3,1), (4,3), (8,4), (6,2), (7,5), (8,7)]
# starrows = [(3, 1), (4, 3), (8,4), (6,2), (7,5)]

# arrows_1 = [(3,1), (4,3), (8,4), (6,2), (7,5), (8,7), (8,6)]

# pos = {1: 1, 2: 1, 5: 1, 3: 2, 6: 2, 7: 2, 4: 3, 8: 4}


mapping = []

# for i in range(6):
#     mapping.append((6, i+1))
# for i in range(8):
#     mapping.append((8, i+1))
# for i in range(10):
#     mapping.append((10, i+1))
# # for i in range(11):
# #     mapping.append((11, i+1))

for i in range(4):
    mapping.append((4, i+1))
for i in range(7):
    mapping.append((7, i+1))
for i in range(9):
    mapping.append((9, i+1))
for i in range(11):
    mapping.append((11, i+1))


# arrows = [(4,1), (7,4), (9, 7), (10, 9), (5, 2), (8,5), (6,3), (10,6)]
# starrows = [(4,1), (7,4), (9, 7), (10, 9), (5, 2), (8,5), (6,3)]

# arrows_1 = [(4,1), (7,4), (9, 7), (10, 9), (5, 2), (8,5), (6,3), (10,6), (10, 8)]



# arrows_1 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 6)]
# arrows_2 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9), (10, 8), (10, 7)]

starrows = [(5,1), (8,5), (10,8), (11, 10), (6,2), (9, 6), (7,3)]
arrows = [(5,1), (8,5), (10,8), (11, 10), (6,2), (9, 6), (7,3), (10,7), (9,4)]

# pos = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9:4, 10: 5}

pos = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9:3, 10: 4, 11:5}

print(fast_experiment(mapping, arrows, starrows, pos, 11, 31, {0, 1, 4, 5, 7}))
# print(fast_experiment(mapping, arrows_1, starrows, pos, 10, 24, {0, 1, 3, 4, 6, 8}))
# print(fast_experiment(mapping, arrows, starrows, pos, 10, 24, {0, 1, 3, 4, 6, 8}))




# mapping = [(5, 1), (5, 2), (5, 5), (6, 1), (6, 2), (6, 5), (6, 3), (6, 6), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
# arrows = [(3, 1), (4, 3), (6, 2), (7, 4), (7, 5), (7,6)]
# starrows = [(3, 1), (4, 3), (6, 2), (7, 4)]

# pos = {1: 1, 2: 1, 3: 2, 4: 3, 5: 1, 6: 2, 7: 4}

# print(fast_experiment(mapping, arrows, starrows, pos, 7, 15, 4))

# print(fast_experiment(mapping, arrows, starrows, pos, 8, ))
# print(fast_experiment(mapping, arrows_1, starrows, pos, 7, 15, 4))
