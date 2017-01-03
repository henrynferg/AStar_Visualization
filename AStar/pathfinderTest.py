"""
Henry Ferguson -- the tests for the pathfinder algorithm.
It passes the eye test when I run the full program, tests seem ok, too.
"""

import Square
import tkinter
from AStarPathfinder import *

sqList = []

for y in range(10):
    sqRow = []
    for x in range(10):
        sqRow.append(Square.Square(3, x*10, y*10))
    sqList.append(sqRow)

print("Distances:")

sq1 = sqList[0][1]
sq2 = sqList[0][1]
print(distance(sq1, sq2)) # Should be 0
sq2 = sqList[0][2] # Should be root 10^2, or 10.
print(distance(sq1, sq2))
sq2 = sqList[1][2] # Should be root(10^2+10^2). Calculator shows 14.14.
print(distance(sq1, sq2))

print("Neighbors:")

upperLeftCorner = sqList[0][0].neighbors
lowerRightCorner = sqList[len(sqList)-1][len(sqList)-1].neighbors
middle = sqList[1][1].neighbors

setSquareNeighbors(sqList) # Looking for reasonable x, y values in
                           # following lines.
for sq in upperLeftCorner:
    print("Upper-lefthand corner neighbor x y:", sq.x, sq.y) 
    # (0, 1) (1, 0) (1, 1) only -- x, y values are x10.
for sq in lowerRightCorner:
    print("Lower-righthand corner neighbor x y:", sq.x, sq.y) # 3 points
for sq in middle:
    print("(1,1) neighbor x y:", sq.x, sq.y) # 8 pts., all permutations of 
                                       #(0-2, 0-2) excluding (1, 1)

print("Path:")
root = tkinter.Tk()
can = tkinter.Canvas()
#path1=AStar(sqList[0][0], sqList[0][5], can) # should be only nodes on row 0
#path2 = AStar(sqList[5][5], sqList[9][9], can) # should be diagonal
# Walls in the way
#sqList[1][1].isImpassible = True
#sqList[1][0].isImpassible = True
#sqList[1][2].isImpassible = True
#path3 = AStar(sqList[0][1], sqList[5][1], can)
# No valid path.
sqList[1][0].isImpassible = True
sqList[0][1].isImpassible = True
sqList[1][1].isImpassible = True
try:
    breadth_first_search(sqList[0][0], sqList[2][2], can)
except(Exception):
    print("No path BFS")

try:
    AStar(sqList[0][0], sqList[2][2], can)
except(Exception):
    print("No path A*")
root.destroy()
#print("Path one: (0,0)-(0,5)")
#for node in path1:
#    print(node.x, node.y) # 10*position in list -- in reverse order
#print("Path two: (5,5)-(9,9)")
#for node in path2:
#    print(node.x, node.y)
#print("Path three: (0,1)-(5,1), wall in the way")
#for node in path3:
#    print(node.x, node.y)


