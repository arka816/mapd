## MULTI AGENT PICKUP AND DELIVERY
## OPTIMAL ALGORITHM USING
## TASK BASED CONFLICT SEARCH

INT_MIN = float('-inf')
INT_MAX = float('inf')

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

cache = [[-1 for j in range(M*N)] for i in range()]

def expand(s, collisions=None):
    # EXPANDS A NODE ACCORDING TO STATE TRANSFORMATION RULES
    children = []
    assignedTasks = []
    for tasks in s['task']:
        assignedTasks += tasks
    if collisions:
        for agent in collisions:
            curr = deepcopy(s)
            curr['avoidlist'][agent] += collisions[agent]
            curr['collisions'] = True
            children.append(curr)
        pass
    else:
        for task in range(n):
            if task not in assignedTasks:
                for agent in range(m):
                    curr = deepcopy(s)
                    curr['tasks'][agent].append(task)
                    curr['collisions'] = False
                    children.append(curr)
                    
    return children

def checkGoal(s):
    # CHECKS IF GOAL NODE IS REACHED
    if s['collisions']:
        return False
    assignedTasks = []
    for tasks in s['task']:
        assignedTasks += tasks
    if len(assignedTasks) != n:
        return False
    return True

def distance(src, dest):
    # CHECKS CACHE FOR DISTANCE
    # CALCULATES A HEURISTIC ESTIMATE OF DISTANCE FROM SOURCE TO DESTINATION
    # USING MANHATTAN DISTANCE
    c = cache[N*src[0] + src[1]][N*dest[0] + dest[1]] 
    if c == -1:
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])
    else:
        return c

def heuristics(s):
    heuristics = [0 for i in range(m)]
    assignedTasks = []
    for tasks in s['task']:
        assignedTasks += tasks
    for task in range(n):
        if task not in assignedTasks:
            # ASSIGN TASK TO CLOSEST AGENT
            closestAgent = 0
            closestDistance = INT_MAX
            for agent in range(m):
                if len(s['tasks'][agent]) > 0:
                    d = distance(D[s['tasks'][agent][-1]], P[task])
                    if d < closestDistance:
                        closestDistance = d
                        closestAgent = agent
            # UPDATE THE HEURISTICS FOR EACH AGENT
            heuristics[closestAgent] += distance(D[s['tasks'][closestAgent][-1]], P[task]) + distance(P[task], D[task])
    
    return heuristics



    









