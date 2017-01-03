# AStar_Visualization
A visualization of the A* algorithm in Tkinter.
Henry Ferguson -- Macalester College, Algorithm Design & Analysis final project, Fall 2016.

ASTAR

This is a pathfinding visualization with a brute-force breadth-first search algorithm and a greedy A* algorithm. Each algorithm finds a path
between the start square and the end square, travelling left, right, up, down, and diagonally.

Make sure Python is installed and added to the path.

This program has not been tested with Python 2 or lower.

To run this program, download it, open the terminal, cd to where this folder is installed, and type in "python AStar.py" without the quotes.
This program only uses the Python standard library (Tkinter, heapq, math, sys modules), so there are no special build instructions.
A GUI with three buttons and a canvas filled with blue squares should come up. Follow the instruction label on the GUI to run the program.

There are many different square colors the program uses. Here are what they mean:

Blue = normal square
Yellow = starting square
Orange = goal square
Green = path the algorithm found
Red = squares the algorithm checked that were not part of the path.
