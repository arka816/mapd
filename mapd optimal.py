## MULTI AGENT PICKUP AND DELIVERY
## OPTIMAL ALGORITHM USING
## TASK BASED CONFLICT SEARCH

INT_MIN = float('-inf')
INT_MAX = float('inf')

from astar import AStar
from task_parser import parseTask
from copy import deepcopy

#INPUTS
M, N, grid, m, n, agentsData, taskData = parseTask()

S = [d[0] for d in agentsData]
E = [d[1] for d in agentsData]
P = [d[0] for d in taskData]
D = [d[1] for d in taskData]


cache = [[[] for j in range(M*N)] for i in range(M*N)]

astar = AStar(deepcopy(grid))

class Node:
    def __init__(self):
        self.tasks = [[] for i in range(m)]
        self.avoidlist = [[] for i in range(m)]
        self.g = [0 for i in range(m)]
        self.h = [0 for i in range(m)]
        self.F = 0
        self.paths = []
        self.collision = None
    def equals(self, other):
        return self.tasks == other.tasks and self.avoidlist == other.avoidlist

def expand(s):
    # EXPANDS A NODE ACCORDING TO STATE TRANSFORMATION RULES
    children = []
    assignedTasks = [task for tasks in s.tasks for task in tasks]
    if s.collision:
        i, j, x, y, t = s.collision
        curr = Node()
        curr.tasks = deepcopy(s.tasks)
        curr.avoidlist[i].append((x, y, t))
        children.append(curr)
        curr = Node()
        curr.tasks = deepcopy(s.tasks)
        curr.avoidlist[j].append((x, y, t))
        children.append(curr)
    else:
        for task in range(n):
            if task not in assignedTasks:
                for agent in range(m):
                    curr = Node()
                    curr.tasks = deepcopy(s.tasks)
                    curr.tasks[agent].append(task)
                    children.append(curr)       
    return children

def checkGoal(s):
    # CHECKS IF GOAL NODE IS REACHED
    if s.collision:
        return False
    assignedTasks = [task for tasks in s.tasks for task in tasks]
    if len(assignedTasks) != n:
        return False
    return True

def distance(src, dest):
    # CHECKS CACHE FOR DISTANCE
    # CALCULATES A HEURISTIC ESTIMATE OF DISTANCE FROM SOURCE TO DESTINATION
    # USING MANHATTAN DISTANCE
    c = len(cache[N*src[0] + src[1]][N*dest[0] + dest[1]])
    if c == 0:
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])
    else:
        return c

def heuristics(s):
    heuristics = [0 for i in range(m)]
    assignedTasks = [task for tasks in s.tasks for task in tasks]
    tasks = deepcopy(s.tasks)
    
    for task in range(n):
        if task not in assignedTasks:
            # ASSIGN TASK TO CLOSEST AGENT
            closestAgent = 0
            closestDistance = INT_MAX
            for agent in range(m):
                if len(tasks[agent]) > 0:
                    d = distance(D[tasks[agent][-1]], P[task])
                    if d < closestDistance:
                        closestDistance = d
                        closestAgent = agent
            # UPDATE THE HEURISTICS FOR EACH AGENT
            tasks[closestAgent].append(task)
            heuristics[closestAgent] += distance(D[s.tasks[closestAgent][-1]], P[task]) + distance(P[task], D[task])
    
    for agent in range(m):
        if len(tasks[agent]) > 0:
            heuristics[agent] += distance(D[tasks[agent][-1]], E[agent])
    
    return heuristics


def planPath(src, tasks, avoidList):
    # PLANS PATH FOR SINGLE AGENT
    path = []
    if len(tasks) == 0:
        return path
    last = src
    for task in tasks:
        # CACHE CANNOT BE USED SINCE PATHS ARE PLANNED ACCORDING TO AVOID LISTS
        # PLAN LAST TO PICKUP
        subpath = astar.findBestPath(last, P[task], avoidList, len(path))
        path += subpath[:-1]
        
        # PLAN PICKUP TO DELIVERY
        subpath = astar.findBestPath(P[task], D[task], avoidList, len(path))
        path += subpath[:-1]
        
        last = D[task]
    path.append(last)
    return path

def planPaths(s):
    # PLANS PATH FOR ALL AGENTS AND CHECKS FOR COLLISIONS
    paths = [planPath(S[agent], s.tasks[agent], s.avoidlist[agent]) for agent in range(m)]
    collision = None
    for i in range(m):
        for j in range(i+1, m):
            path_i, path_j = paths[i], paths[j]
            k = 1
            while k < len(path_i) and k < len(path_j):
                if path_i[k] == path_j[k] and grid[path_i[k][0]][path_i[k][1]] != 2 and path_i[k] not in S and path_i[k] not in E:
                    collision = (i, j, path_i[k][0], path_i[k][1], k-1)
                    break
                k += 1
    return paths, collision


def search():
    # SEARCHES THE TASK BASED CONFLICT TREE USING A*
    start = Node()
    
    openset = set()
    closedset = set()
    current = start
    openset.add(current)
    
    while len(openset) > 0:
        current = min(openset, key=lambda o:o.F)
        if checkGoal(current):
            makespan = max([len(path) for path in current.paths])
            return current.tasks, makespan
        
        openset.remove(current)
        closedset.add(current)
        
        for node in expand(current):
            node.paths, node.collision = planPaths(node)
            if node in closedset or node in openset:
                pass
            else:
                node.h = heuristics(node)
                node.g = [len(path) - 1 for path in node.paths]
                node.F = max([node.h[i] + node.g[i] for i in range(m)])
                openset.add(node)
    
    
tasks, makespan = search()
print(tasks)
print(makespan)
        
astar.findBestPath([0, 0], [0, 6], [(0, 3, 2),], 0)









