"""
Made by Henry Ferguson as the final project for Macalester's COMP 221 
(Algorithm Design & Analysis) class, Fall 2016.

A* is a pathfinding algorithm. It is designed to find a path through
obstacles from a starting node to a goal node by minimizing 2 costs: a 'G' 
cost and an 'H' cost. A node's H cost is how far away the node is from
the goal node. A node's G cost, calculated when its neighbor is visited,
is how far away the node is from its neighbor. These two values together
make up a node's 'F' cost. The algorithm then uses a heap to get the
neighboring node with the least F cost. When the algorithm gets the goal
node, it then reconstructs the path by backtracking.
"""

import Square, math, heapq

green = "#00F000"
red = "#F00000"
orange = "#FF9600"

def AStar(start, end, canvas):
    """Returns a path of nodes from the 'start' parameter to the 'end'
    parameter."""
    initialDistance = distance(start, end)
    workHeap = [start]
    closedList = []
    start.fCost = initialDistance
    start.gCost = 0
    while len(workHeap) > 0:
        node = heapq.heappop(workHeap)
        for neighbor in node.neighbors:
            neighbor.gCost = distance(node, neighbor) + node.gCost
            neighbor.fCost = distance(neighbor, end) + neighbor.gCost
            if (neighbor.isImpassible):
                pass
            elif neighbor in closedList:
                pass
            elif neighbor in workHeap:
                pass
            else:
                neighbor.parent = node
                heapq.heappush(workHeap, neighbor)

        closedList.append(node)
        if node is not start and node is not end:
            node.color = red
            canvas.create_rectangle(node.x, node.y,
                                node.x+node.side, node.y+node.side,
                                fill = node.color)
        if node is end:
            return makePath(node, canvas)
    raise("Couldn't find a valid path.")

def breadth_first_search(start, end, canvas):
    """Finds a path from the start to the end by doing breadth-first search.
    Changes the colors of squares on CANVAS."""
    work = [start]
    closedList = []
    while len(work) != 0:
        current = work.pop(0)
        if current is end:
            return makePath(current, canvas)

        for neighbor in current.neighbors:
            if neighbor not in closedList and neighbor not in work:
                if not neighbor.isImpassible:
                    neighbor.parent = current
                    work.append(neighbor)

        if current is not start:
            current.color = red
            canvas.create_rectangle(current.x, current.y,
                                current.x+current.side,
                                current.y+current.side,
                                fill = current.color)
        closedList.append(current)
    raise("Couldn't find a valid path.")

def makePath(current, canvas):
    """Backtracks to find the path from the starting node to the goal
    node."""
    finalPath = []
    while current.parent is not None:
        if current.color != orange: # If the node isn't the start node
            current.color = green
            canvas.create_rectangle(current.x, current.y,
                                    current.x+current.side,
                                    current.y+current.side,
                                    fill = current.color)
        current = current.parent
        finalPath.append(current)
    return finalPath

def setSquareNeighbors(sqList):
        """Sets the neighbor nodes of each square in sqList."""
        for i in range(len(sqList)):
            for j in range(len(sqList[i])):
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if (x != 0 or y != 0) and (i+x >= 0 and j+y >= 0):
                            try:
                                sqList[i][j].neighbors.append(sqList[i+x][j+y])
                            except(IndexError):
                                pass

def distance(node1, node2):
    """Parameters: two nodes.
    returns: the euclidian distance between the two nodes."""
    return math.sqrt((node2.x-node1.x)**2 + (node2.y-node1.y)**2)
