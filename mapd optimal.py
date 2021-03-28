## MULTI AGENT PICKUP AND DELIVERY
## OPTIMAL ALGORITHM USING STATE SPACE FORMULATION

from copy import deepcopy

#INPUTS
agentsData = [
        [[0, 0], [0, 8]],
        [[5, 9], [5, 5]],
        [[0, 0], [5, 5]]
    ]
taskData = [
        [[5, 0], [3, 12]],
        [[4, 6], [0, 6]],
        [[5, 0], [0, 6]]
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
P = [d[0] for d in taskData]
D = [d[1] for d in taskData]


m, n = len(agentsData), len(taskData)
M, N = len(grid), len(grid[0])

finalProdStat = [-2 for i in range(n)]
visitedArrays = [[[False for j in range(N)] for i in range(M)] for k in range(m)]

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

def reset(arr):
    R, C = len(arr), len(arr[0])
    for i in range(R):
        for j in range(C):
            arr[i][j] = False
    

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
        p = deepcopy(robotPos)
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


        
def assignTasks(taskArray, taskAllotments, index, allotment, allotted):
    if index == len(taskArray):
        if len(allotment) > 0:
            taskAllotments.append(allotment)
        return
    if len(taskArray[index]) == 0:
        assignTasks(taskArray, taskAllotments, index + 1, allotment, allotted)
    else:
        for task in taskArray[index]:
            if not allotted[task]:
                a = deepcopy(allotment)
                b = deepcopy(allotted)
                b[task] = True
                a.append([index, task])
                assignTasks(taskArray, taskAllotments, index + 1, a, b)
    return
    
        

def search(q):
    ### ITERATIVE BFS OVER SEARCH SPACE TREE
    while len(q) > 0:
        curr = q.pop(0)
        robotPos = curr["robotPos"]
        prodStat = curr["prodStat"]
        robotStat = curr["robotStat"]
        assignment = curr["assignment"]
        visited = curr['visited']
    
        ## check if goal state  E and 
        if robotPos == E: #and prodStat == finalProdStat:
            return assignment
    
        nextStates = transformState(robotPos, visited)
        print(prodStat, robotPos)
        
        for nextRobotPos in nextStates:
            ps = deepcopy(prodStat)
            rs = deepcopy(robotStat)
            ass = deepcopy(assignment)
            v = deepcopy(visited)
            
            taskArray = [[] for i in range(m)]            
            
            for i in range(m):
                pos = nextRobotPos[i]
                v[i][pos[0]][pos[1]] = True
                
                ## DELIVERY
                if rs[i] == 0:
                    # if robot is occupied
                    try:
                        J = [j for j, p in enumerate(D) if p == pos and ps[j] == i]
                        if len(J) > 0:
                            j = J[0]
                            reset(v[i])
                            ps[j] = -2
                            rs[i] = 1
                    except:
                        pass
                
                ## PICKUP
                if rs[i] == 1:
                    # if robot is free
                    try:
                        J = [j for j, p in enumerate(P) if p == pos and ps[j] == -1]
                        if len(J) > 0:  
                            rs[i] = 0
                            reset(v[i])
                        taskArray[i] = J
                    except:
                        pass
                
            allotment = []
            allotted = [False for i in range(n)]
            taskAllotments = []
            assignTasks(taskArray, taskAllotments, 0, allotment, allotted)
            
            
            if len(taskAllotments) > 0:
                ## if there are possible task allotments branch further
                for allotment in taskAllotments:
                    ps_curr = deepcopy(ps)
                    ass_curr = deepcopy(ass)
                    for item in allotment:
                        i, j = item
                        ps_curr[j] = i
                        if i in ass_curr:
                            ass_curr[i].append(j)
                        else:
                            ass_curr[i] = [j]
                    q.append({"robotPos": nextRobotPos, "prodStat": ps_curr, "robotStat": deepcopy(rs), "assignment": ass_curr, "visited": deepcopy(v)})
            else:
                ## if there are no possible task allotments no further branching
                q.append({"robotPos": nextRobotPos, "prodStat": ps, "robotStat": rs, "assignment": ass, "visited": v})
    return "queue exhausted"


initialState = {"robotPos": S, "prodStat": [-1 for i in range(m)], "robotStat": [1 for i in range(n)], "assignment": dict(), "visited": visitedArrays}
q = [initialState]
assignment = search(q)
if assignment == -1:
    print("no solution")
else:
    print(assignment)
    
