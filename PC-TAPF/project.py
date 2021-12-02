class OTGNode:
    def __init__(self) -> None:
        self.parents = []
        self.children = []

    def addParent(self, parent) -> None:
        self.parents += parent

    def addChild(self, child) -> None:
        self.children += child

class operation(OTGNode):
    def __init__(self, inputs, outputs, duration) -> None:
        # inputs   : inputs required for the operation
        # outputs  : output(/s) of the operation
        # duration : time taken by the operation
        super().__init__()
        self.inputs = inputs
        self.outputs = outputs
        self.duration = duration

class object(OTGNode):
    def __init__(self, start, goal, collect, deposit) -> None:
        # start   : initial location of object (pickup)
        # goal    : target location of object (delivery)
        # colect  : time required for any robot to collect the object
        # deposit : time required for any robot to deposit the object
        super().__init__()
        self.start = start
        self.goal = goal
        self.collect = collect
        self.deposit = deposit


class Project:
    def __init__(self, agents, objects, operations) -> None:
        # agents     : number of robots
        # objects    : number of objects to pick up and deliver
        # operations : number of manufacturing operations/stations
        self.agents = agents
        self.objects = objects
        self.operations = operations

    def parser(self, filename) -> None:
        # filename : file name of the task file
        # grid     : grid design of the workspace
        # otg      : operation task graph

        self.grid_size_X, self.grid_size_Y = len(grid), len(grid[0])
        self.grid = grid
        self.otg = otg