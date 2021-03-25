class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 0
        
def children(point, grid):
    x,y = point.x, point.y
    return [Node(p.x, p.y) for p in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)] if grid[p.x][p.y] != 0]

def manhattan(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y -p2.y)

def aStar(start, goal, grid, avoidlist):
    # PLANS THE PATH FROM SRC TO DEST
    # WITHOUT MAKING MOVES MENTIONED IN THE AVOID LIST
    # USING A* ALGORITHM
    openset = set()
    closedset = set()
    current = start
    openset.add(current)
    
    while len(openset) > 0:
        current = min(openset, key=lambda o:o.G + o.H)
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        

        openset.remove(current)
        closedset.add(current)
        
        for node in children(current, grid):
            if node in closedset:
                continue
            if node in openset:
                new_g = current.G + 1
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
            else:
                node.G = current.G + 1
                node.H = manhattan(node, goal)
                node.parent = current
                openset.add(node)
                
    raise ValueError('No Path Found')
    
