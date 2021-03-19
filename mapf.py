## MULTI AGENT PATH FINDING
## OPTIMAL ALGORITHM USING STATE SPACE FORMULATION

from copy import deepcopy

#INPUTS
agentsData = [
        [[0, 0], [0, 8]],
        [[5, 9], [5, 5]],
        [[0, 0], [5, 5]]
    ]
grid = [
        [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

S = [d[0] for d in agentsData]
E = [d[1] for d in agentsData]


m = len(agentsData)
M, N = len(grid), len(grid[0])

visitedArrays = [[[False for j in range(N)] for i in range(M)] for k in range(m)]

for i in range(m):
    x, y = S[i]
    visitedArrays[i][x][y] = True

combinations = []
def generateAgentCombinations(curr, size):
    if size == m:
        combinations.append(curr)
        return
    newCurr = curr + [size]
    generateAgentCombinations(curr, size + 1)
    generateAgentCombinations(newCurr, size + 1)
    return

generateAgentCombinations([], 0)
combinations.pop(0)


def combineMoves(robotPos, i, nextStates, transformations):
    keys = list(transformations.keys())
    if i == len(keys):
        ## check for collisions and then push into nextStates
        flag = True
        duplicates = [p for p in robotPos if robotPos.count(p) > 1]
        for p in duplicates:
            if grid[p[0]][p[1]] != 2:
                flag = False
                break
        if flag:
            nextStates.append(robotPos)
        return
    index = keys[i]
    for move in transformations[index]:
        p = robotPos.copy()
        p[index] = move
        combineMoves(p, i+1, nextStates, transformations)
    return


def transformState(robotPos, visited):
    nextStates = []
    for combination in combinations:
        ## CHANGE THE CONFIGURATIONS ONLY OF THE ROBOTS IN THIS COMBINATION
        transformations = dict()
        for index in combination:
            ## FIND ALL POSSIBLE MOVES FOR THIS ROBOT
            moves = []
            x, y = robotPos[index]
            if x - 1 >= 0 and grid[x-1][y] != 0 and not visited[index][x-1][y]:
                moves.append([x-1, y])
            if x + 1 < M and grid[x+1][y] != 0 and not visited[index][x+1][y]:
                moves.append([x+1, y])
            if y - 1 >= 0 and grid[x][y-1] != 0 and not visited[index][x][y-1]:
                moves.append([x, y-1])
            if y + 1 < N and grid[x][y+1] != 0 and not visited[index][x][y+1]:
                moves.append([x, y+1])
            transformations[index] = moves
        combineMoves(robotPos, 0, nextStates, transformations)
    return nextStates

        

def search(q):
    ### ITERATIVE BFS OVER SEARCH SPACE TREE
    while len(q) > 0:
        curr = q.pop(0)
        robotPos = curr["robotPos"]
        visited = curr['visited']
    
        ## check if goal state is reached
        if robotPos == E: 
            return assignment
    
        nextStates = transformState(robotPos, visited)
        
        print(robotPos)
        
        for nextRobotPos in nextStates:
            v = deepcopy(visited)
            for i in range(m):
                pos = nextRobotPos[i]
                v[i][pos[0]][pos[1]] = True
            q.append({"robotPos": nextRobotPos, "visited": v, "parent": curr})
    return "queue exhausted"


initialState = {"robotPos": S, "visited": visitedArrays, "parent": None}
q = [initialState]
assignment = search(q)
if assignment == -1:
    print("no solution")
else:
    print(assignment)
    
