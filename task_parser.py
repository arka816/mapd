def parseTask(filename='demo.task'):
    f = open(filename, 'r')

    M, N = [int(item) for item in f.readline().strip().split(" ")]
    
    grid = []
    agentsData = []
    taskData = []
    
    for i in range(M):
        row = [int(item) for item in f.readline().strip().split()]
        grid.append(row)
        
    m = int(f.readline().strip())
    
    for i in range(m):
        row = [int(item) for item in f.readline().strip().split()]
        agentsData.append([row[:2], row[2:]])
        
    n = int(f.readline().strip())
    
    for i in range(n):
        row = [int(item) for item in f.readline().strip().split()]
        taskData.append([row[:2], row[2:]])
        
    return M, N, grid, m, n, agentsData, taskData