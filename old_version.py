from itertools import product, combinations
import math

#convention: i -> j


def candidates(i, j, stindic, indic, outdic):
    k = stindic[i]
    if k==-1 : return (-1, [])

    result = []
    for l in outdic[k]:
        if l != i:
            result.append((l, j))

    for m in indic[j]:
        result.append((k, m))
    
    return (k, result)

    




#filling the entries by solving the others recursively
def evaluate(i, j, solved, visited, matrix, stindic, stoutdic, indic, outdic):
    if solved[i][j] == True:
        visited[i][j] = False
        return matrix[i][j]
    
    if visited[i][j] == True:
        print("cycle at", (i, j))
        raise ValueError("cycle")

    visited[i][j] = True
    sum = 0
    check = True

    if(candidates(i, j, stindic, indic, outdic)[0] == -1):
      
        solved[i][j] = True
        visited[i][j] = False
        return matrix[i][j]
    
    if len(candidates(i, j, stindic, indic, outdic)[1])==0:
        solved[i][j] = True
        visited[i][j] = False
        matrix[i][j] = 0
        return 0
    
    for pair in candidates(i, j, stindic, indic, outdic)[1]:
        sum = sum + evaluate(pair[0], pair[1], solved, visited, matrix, stindic, stoutdic, indic, outdic)

    visited[i][j] = False
    solved[i][j] = True
    matrix[i][j] = sum

    return sum

def parabolic_check(matrix, mu, size):
    for i in range(mu):
        for j in range(mu, size):
            if matrix[i][j]%2 != 0:
                return False
            
    return True

def test(arr, solved, matrix, visited, pos, mapping, stindic, stoutdic, indic, outdic, size, total, mu):

    solved = [[False for _ in range(size)] for _ in range(size)]
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    visited = [[False for _ in range(size)] for _ in range(size)]
    #incorrect stuff
    for i in range(size):
        for j in range(size):
            if(pos[j+1] > pos[i+1]):
                solved[i][j] = True

    for i in range(total):
        a = mapping[i][0]-1
        b = mapping[i][1]-1
        matrix[a][b] = arr[i]
        solved[a][b] = True
        # visited[a][b] = True

    for i in range(size):
        for j in range(size):
            if solved[i][j] == False:
                matrix[i][j] = evaluate(i, j, solved, visited, matrix, stindic, stoutdic, indic, outdic)
    
    return parabolic_check(matrix, mu, size)


def experiment(mapping, arrows, starrows, pos, size, total, mu):

    stindic = {a: -1 for a in range(size)}
    stoutdic = {a: -1 for a in range(size)}

    indic = {a: [] for a in range(size)}
    outdic = {a : [] for a in range(size)}

    #finding the arrows
    for ar in arrows:
        indic[ar[1]-1].append( ar[0]-1)
        outdic[ar[0]-1].append(ar[1]-1)

    for ar in starrows:
        stindic[ar[1]-1] =ar[0]-1 
        stoutdic[ar[0]-1] =ar[1]-1

    ans = 0
    for arr in product([0, 1], repeat=total):
        solved = [[False for _ in range(size)] for _ in range(size)]
        matrix = [[0 for _ in range(size)] for _ in range(size)]
        visited = [[False for _ in range(size)] for _ in range(size)]
        arr = list(arr)
        if test(arr, solved, matrix, visited, pos, mapping, stindic, stoutdic, indic, outdic, size, total, mu):
            ans += 1


    return ans

mapping = [(9,1), (9,2), (9,7), (9,3), (9,4), (9, 9), (8,1), (8,2), (8,7), (8,3), (8,4), (8, 9), (8,5), (8,8), (10,1), (10,2), (10,7), (10,3), (10,4), (10, 9), (10,5), (10,8), (10, 6), (10,10)]
arrows = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9), (10, 8)]
starrows = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7)]

arrows_1 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9)]
arrows_2 = [(3,1), (5,3), (6,5), (10,6), (4,2), (8,4), (9, 7), (10, 9), (10, 8), (10, 7)]

pos = {1: 1, 2: 1, 7: 1, 3: 2, 4: 2, 9: 2, 5: 3, 8: 3, 6: 4, 10: 5}

print(experiment(mapping, arrows, starrows, pos, 10, 24, 6))
print(experiment(mapping, arrows_1, starrows, pos, 10, 24, 6))
print(experiment(mapping, arrows_2, starrows, pos, 10, 24, 6))
