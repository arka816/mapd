## MULTI AGENT PICKUP AND DELIVERY
## HEURISTIC ALGORITHM USING HAMILTONIAN CYCLES

INT_MIN = float('-inf')
INT_MAX = float('inf')
            
class Cell:
    x = -1
    y = -1
    dist = 0
    def __init__(self, p, distance = 0):
        self.x, self.y = p
        self.dist = distance
     
#INPUTS
agentsData = [
        [[0, 0], [0, 8]],
        [[5, 9], [5, 5]],
        [[0, 0], [5, 5]]
    ]
taskData = [
        [[5, 0], [3, 12]],
        [[4, 6], [0, 5]],
        [[5, 0], [0, 5]]
    ]
grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]


m, n = len(agentsData), len(taskData)
M, N = len(grid), len(grid[0])

adjMat = [[0 for j in range(m+n)] for i in range(m+n)]
vertexType = [0 for i in range(len(agentsData))] + [1 for i in range(len(taskData))]
vertexData = agentsData + taskData


def cellDistance(sp, dp):
    ## FINDS MINIMUM DISTANCE BETWEEN SOURCE CELL AND DESTINATION CELL USING BFS
    ## RETURNS -1 IF NO PATH FOUND
    ## FOR WELL POSED MAPD PROBLEM HOWEVER THERE WILL ALWAYS BE A PATH
    source = Cell(sp, 0)
    dest = Cell(dp, 0)
    visited = [[False for j in range(N)] for i in range(M)]
    q = []
    q.append(source)
    visited[source.x][source.y] = True
    
    while len(q) > 0:
        curr = q.pop(0)
        if curr.x == dest.x and curr.y == dest.y:
            return curr.dist
        
        ## CONSIDER ALL 4 NEIGHBORS AND PUSH THEM TO QUEUE IF THEY ARE NOT OBSTACLES
        if curr.x - 1 >= 0 and not visited[curr.x - 1][curr.y] and grid[curr.x - 1][curr.y] != 0:
            q.append(Cell([curr.x - 1, curr.y], curr.dist + 1))
            visited[curr.x - 1][curr.y] = True
            
        if curr.x + 1 < M and not visited[curr.x + 1][curr.y] and grid[curr.x + 1][curr.y] != 0:
            q.append(Cell([curr.x + 1, curr.y], curr.dist + 1))
            visited[curr.x + 1][curr.y] = True
        
        if curr.y - 1 >= 0 and not visited[curr.x][curr.y - 1] and grid[curr.x][curr.y - 1] != 0:
            q.append(Cell([curr.x, curr.y - 1], curr.dist + 1))
            visited[curr.x][curr.y - 1] = True
        
        if curr.y + 1 < N and not visited[curr.x][curr.y + 1] and grid[curr.x][curr.y + 1] != 0:
            q.append(Cell([curr.x, curr.y + 1], curr.dist + 1))
            visited[curr.x][curr.y + 1] = True
            
    return -1

def buildGraph():
    ## BUILD THE AGENT-TASK GRAPH
    for i in range(m+n):
        for j in range(m+ n):
            u, v = vertexType[i], vertexType[j]
            if u == 0 and v == 1:
                # U = AGENT AND V = TASK
                adjMat[i][j] = cellDistance(vertexData[i][0], vertexData[j][0])
            elif u == 1 and v == 1:
                # U = TASK AND V = TASKvertexData[i][1]
                adjMat[i][j] = cellDistance(vertexData[i][0], vertexData[i][1]) + cellDistance(vertexData[i][1], vertexData[j][0])
            elif u == 1 and v == 0:
                # U = TASK AND V = AGENT
                adjMat[i][j] = cellDistance(vertexData[i][0], vertexData[i][1])
            else:
                # U = AGENT AND v = AGENT
                pass
                
                
def heapPermutation(a, size, perms):
    if size == 1:
        perms.append([0] + a)
        return
    for i in range(size):
        heapPermutation(a, size-1, perms)
        if size & 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]
                
def generateHamiltonianCycles():
    ### GENERATES ALL CYCLIC PERMUTATIONS OF NUMBERS FROM 0 TO m+n-1
    ### SINCE adjMat IS A COMPLETE GRAPH, THIS WILL SIMPLY GENERATE ALL 
    ### POSSIBLE HAMILTONIAN CYCLES
    perms = []
    heapPermutation(list(range(1, m+n, 1)), m + n - 1, perms)
    return perms
    
def getMakespan(cycle):
    a = 0
    for i in range(len(cycle)):
        if vertexType[cycle[i]] == 0:
            a = i
            break

    m = INT_MIN
    cycle = cycle[a:] + cycle[:a]
    t = 0
    
    agent = 0
    
    for i in range(len(cycle) - 1):
        t += adjMat[cycle[i]][cycle[i+1]]
        if vertexType[cycle[i + 1]] == 0:
            ## next item is an agent
            home = cellDistance(vertexData[cycle[i]][1], vertexData[agent][1])
            t += home
            m = max(m, t)
            t = 0
            agent = cycle[i+1]
    t += adjMat[cycle[-1]][cycle[0]] + cellDistance(vertexData[cycle[-1]][1], vertexData[agent][1])
    m = max(m, t)
    return m
    
def getSchedule(cycle):
    a = 0
    for i in range(len(cycle)):
        if vertexType[cycle[i]] == 0:
            a = i
            break
    cycle = cycle[a:] + cycle[:a]
    s, e = 0, 0
    assignments = dict()
    for i in range(len(cycle)):
        if (i+1 < len(cycle) and vertexType[cycle[i + 1]] == 0) or i + 1 == len(cycle):
            e = i
            assignments[cycle[s]] = cycle[s+1: e+1]
            s, e = i+1, i+1
            
    return assignments
    

buildGraph()
minSpan = INT_MAX
index = 0
cycles = generateHamiltonianCycles()

for i in range(len(cycles)):
    cycle = cycles[i]
    span = getMakespan(cycle)
    if span < minSpan:
        minSpan = span
        index = i
        
print("approximate makespan: ", minSpan)
print("schedule", getSchedule(cycles[index]))
