class Node:
    def __init__(self, val, x, y):
        self.val = val
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 0
        
class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.M = len(grid)
        self.N = len(grid[0])
        self.avoidlist = []
        self.offset = 0
        
        for x in range(self.M):
            for y in range(self.N):
                self.grid[x][y] = Node(self.grid[x][y], x, y)
        
    def childrenWithAvoid(self, point, t):
        x,y = point.x, point.y
        children = [self.grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)] if 0 <= d[0] < self.M and 0 <= d[1] < self.N ]
        return [child for child in children if child.val != 0 and (child.x, child.y, t + self.offset) not in self.avoidlist]
    
    def childrenNormal(self, point):
        x,y = point.x, point.y
        children = [self.grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)] if 0 <= d[0] < self.M and 0 <= d[1] < self.N ]
        return [child for child in children if child.val != 0]
    
    @staticmethod
    def manhattan(p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)
    
    def findPathWithAvoid(self, start, goal, avoidlist, offset):
        # PLANS THE PATH FROM SRC TO DEST
        # WITHOUT MAKING MOVES MENTIONED IN THE AVOID LIST
        # USING A* ALGORITHM
        
        start = Node(self.grid[start[0]][start[1]], start[0], start[1])
        goal = self.grid[goal[0]][goal[1]]
        
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        
        while len(openset) > 0:
            current = min(openset, key=lambda o:o.G + o.H)
            if current == goal:
                path = []
                while current.parent:
                    path.append((current.x, current.y))
                    current = current.parent
                path.append((current.x, current.y))
                del openset
                del closedset
                return path[::-1]
            
    
            openset.remove(current)
            closedset.add(current)
            
            for node in self.childrenWithAvoid(current, current.G):
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.G + 1
                    if node.G > new_g:
                        node.G = new_g
                        node.parent = current
                else:
                    node.G = current.G + 1
                    node.H = AStar.manhattan(node, goal)
                    node.parent = current
                    openset.add(node)
                    
        raise ValueError('No Path Found')
        
    def findPathNormal(self, start, goal):
        # PLANS THE PATH FROM SRC TO DEST
        # USING A* ALGORITHM
        
        start = Node(self.grid[start[0]][start[1]], start[0], start[1])
        goal = self.grid[goal[0]][goal[1]]
        
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        
        while len(openset) > 0:
            current = min(openset, key=lambda o:o.G + o.H)
            if current == goal:
                path = []
                while current.parent:
                    path.append((current.x, current.y))
                    current = current.parent
                path.append((current.x, current.y))
                del openset
                del closedset
                return path[::-1]
            
    
            openset.remove(current)
            closedset.add(current)
            
            for node in self.childrenNormal(current):
                if node in closedset:
                    continue
                if node in openset:
                    new_g = current.G + 1
                    if node.G > new_g:
                        node.G = new_g
                        node.parent = current
                else:
                    node.G = current.G + 1
                    node.H = AStar.manhattan(node, goal)
                    node.parent = current
                    openset.add(node)
                    
        raise ValueError('No Path Found')
        
    def findBestPath(self, start, goal, avoidlist, offset):
        # FINDS BEST PATH AMONG THE ONE GENERATED WITH OBSTACLES AND THE ONE GENERATED WITH WAITING
        
        self.avoidlist = avoidlist
        self.offset = offset
        
        avoidPath = self.findPathWithAvoid(start, goal, avoidlist, offset)
        normalPath = self.findPathNormal(start, goal)
        
        collisions = []
        for i in range(len(normalPath)):
            if (normalPath[i][0], normalPath[i][1], offset + i - 1) in avoidlist:
                collisions.append(i)
        if len(avoidPath) > len(normalPath) + len(collisions):
            # WAITING IS A BETTER OPTION
            j = 0
            for i in collisions:
                index = i + j
                normalPath = normalPath[:index] + [normalPath[index-1]] + normalPath[index:]
                j += 1
            return normalPath
        else:
            # CIRCUMVENTING IS A BETTER OPTION
            return avoidPath
        
        
