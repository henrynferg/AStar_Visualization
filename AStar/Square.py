class Square:
    blue = "#0000F0"
    green = "#00F000"
    grey = "#909090"

    def __init__(self, side, x, y, color=blue):
        self.side = side
        self.x = x
        self.y = y
        self.color = color
        self.neighbors = []
        self.isImpassible = False # Can pass thru any square by default.
        self.parent = None # Node that was processed before the current one
        self.fCost = None # Distance from node to goal
        self.gCost = None # Distance from node to parent

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.fCost < other.fCost
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return other.fCost < self.fCost
        return NotImplemented
