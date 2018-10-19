"""
Henry Ferguson

Creates the UI and sets critical parts of the program. Run the program
from this file.
"""

import AStarPathfinder, sys, Square
if sys.version_info[0] == 3:
    print("Python 3 detected.")
    import tkinter as tk
elif sys.version_info[0] <= 2:
    print("Python 2 or lower detected. If the program does not work, \
please start it in Python 3.")
    import Tkinter as tk

length = 18 # Side length for each square in the array -- needs to be int.
spacing = 1 # Amount of space between each square -- needs to be int
window_height = 600
window_length = 800
start = None
goal = None
blue = "#0000F0"
black = "#000000"
green = "#00F000"
red = "#F00000"
yellow = "#FFFF00"
orange = "#FF9600"
squareList = []
already_executed = False  # Goes to 1 if the program was 
                          # run with another algorithm
step = 1 # Step 1: click to set starting square. Step 2: click to set
         # destination square. Step 3: click on multiple blocks/click+drag
         # to set barriers.

class Interface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.buildSquareList()
        self.makeSquares(squareList)

    def create_widgets(self):
        self.labelText = tk.StringVar()
        self.canvas = tk.Canvas(self.master, height=window_height, 
                                width=window_length)
        
        self.run = tk.Button(self,width=9, text="A*", command=self.runAStar)
        self.run.grid(row=3, column=0)

        self.bfs = tk.Button(self, width=9, text="Brute-Force",
                             command=self.runBFS)
        self.bfs.grid(row=2, column=0)

        self.reset_btn = tk.Button(self, width=9, text="Reset", 
                                command=self.reset)
        self.reset_btn.grid(row=1, column=0)

        self.labelText.set("Welcome! Click a square to set the starting\
 point.")
        self.instructions = tk.Label(self, textvariable=self.labelText)
        self.instructions.grid(row=0, column=0)

        self.canvas.grid(row=1, column=0)
        self.canvas.bind('<Button-1>', self.executeInstructions)
        self.canvas.bind('<B1-Motion>', self.executeInstructions)
        self.canvas.bind('<Button-3>', self.resetSquare)
        self.canvas.bind('<B3-Motion>', self.resetSquare)

    def buildSquareList(self):
        """Makes a 2-D list of blue, passable Squares with side length 
        'length' that are 'spacing' pixels apart. Fits as many squares into 
        the canvas as possible."""
        global squareList
        squareRow = []
        row = 0
        col = 0
        while(length + row*length + spacing*row < 
                int(self.canvas['height'])):

            if(length + col*length + spacing*col > 
                    int(self.canvas['width'])):

                col = 0
                row += 1
                squareList.append(squareRow)
                squareRow = []

            newSquare = Square.Square(length, length*col+spacing*col,
                                length*row+spacing*row)
            newSquare.color = blue
            squareRow.append(newSquare)
            col += 1

        AStarPathfinder.setSquareNeighbors(squareList)

    def makeSquares(self, sqList):
        """Creates the squares on squareList the interface's canvas."""
        for allSquares in sqList:
            for squares in allSquares:
                r=self.canvas.create_rectangle(squares.x, squares.y,
                                        squares.x+squares.side,
                                        squares.y+squares.side,
                                        fill = squares.color)

    def makeImpassible(self, node):
        """Makes the parameter node impassible and turns it black."""
        node.color = black
        node.isImpassible = True
        self.canvas.create_rectangle(node.x, node.y,
                                        node.x+node.side,
                                        node.y+node.side,
                                        fill = node.color)

    def makeStart(self, node):
        """Sets the parameter node to be the starting node"""
        global step, start
        node.color = yellow
        start = node
        self.canvas.create_rectangle(start.x, start.y,
                                        start.x+start.side,
                                        start.y+start.side,
                                        fill = start.color)
        step += 1

    def setGoal(self, node):
        """Sets the parameter node to be the goal node."""
        global step, goal
        node.color = orange
        goal = node
        self.canvas.create_rectangle(goal.x, goal.y,
                                        goal.x+goal.side,
                                        goal.y+goal.side,
                                        fill = goal.color)
        step += 1

    def findSquare(self, mouseX, mouseY):
        """Finds the square at a given mouse position.
            If there is no square at the pointed position, returns None"""
        xIndex = (int(mouseX) - (int(mouseX) % (length+spacing))) // (length
                                                                    +spacing)
        yIndex = (int(mouseY) - (int(mouseY) % (length+spacing))) // (length
                                                                    + spacing)
        if (int(mouseX) < length*xIndex+spacing) or int(mouseY) < (length
                                                                *yIndex
                                                                +spacing):
            return None
        return squareList[yIndex][xIndex]

    def resetSquare(self, event):
        """When right clicked, a wall square gets reset to be passible 
        again."""
        clickedSquare = self.findSquare(event.x, event.y)
        if clickedSquare is not None and clickedSquare.isImpassible:
            clickedSquare.isImpassible = False
            clickedSquare.color = blue
            self.canvas.create_rectangle(clickedSquare.x, clickedSquare.y,
                                        clickedSquare.x+clickedSquare.side,
                                        clickedSquare.y+clickedSquare.side,
                                        fill = clickedSquare.color)

    def executeInstructions(self, event):
        """The 'step' variable determines what this function does:
            if the step variable is 1, clicking on a square assigns the
            starting node and increments step. If the step variable is 2, 
            clicking a square assigns the destination node and increments 
            step. If the step variable is 3, clicking squares makes them 
            impassible. Updates the instructions label on the UI."""

        clickedSquare = self.findSquare(event.x, event.y)
        if clickedSquare is not None and clickedSquare.color == blue:
            if step == 1:
                self.makeStart(clickedSquare)
                self.labelText.set("Now, click another square to make the\
 destination square.")

            elif step == 2:
                self.setGoal(clickedSquare)
                self.labelText.set("Click and drag to set barriers. click\
 'A*' to run the A* pathfinder or 'Brute-Force' to run a DFS pathfinder.\
 Right click to remove wall squares.")

            else:
                self.makeImpassible(clickedSquare)

    def runAStar(self):
        """Executes when the 'A*' button is clicked. Runs the A star
        algorithm and draws the found path in green."""
        global already_executed
        if already_executed:
            self.soft_reset()

        if start is not None and goal is not None:
            try:
                path = AStarPathfinder.AStar(start, goal, self.canvas)
                self.labelText.set("KEY: Red = checked and not path,\
 green = path. Click 'Reset' to reset the board and go again.")
                already_executed = True
            except(Exception):
                self.labelText.set("Could not find a valid path.")

    def runBFS(self):
        """Executes when the 'Brute-Force' button is clicked. Runs the BFS
        algorithm and draws the found path in green."""
        global already_executed
        if already_executed:
            self.soft_reset()

        if start is not None and goal is not None:
            try:
                path = AStarPathfinder.breadth_first_search(start, goal,
                                                            self.canvas)
                self.labelText.set("KEY: Red = checked and not path,\
 green = path. Click 'Reset' to reset the board and go again.")
                already_executed = True
            except(Exception):
                self.labelText.set("Could not find a valid path.")

    def soft_reset(self):
        """Keeps all squares, but makes once-red or green squares blue.
        Runs when the user re-runs an algorithm on the same map."""
        global already_executed, squareList
        for squareRow in squareList:
            for square in squareRow:
                if square.color == red or square.color == green:
                    square.color = blue
        self.makeSquares(squareList)
        already_executed = False

    def reset(self):
        """Executed when the 'reset' button is clicked. Sets all squares to
        be blue and passible, and redraws them on the canvas."""
        global already_executed, squareList
        already_executed = False
        squareList = []
        self.resetInstructions()
        self.buildSquareList()
        self.makeSquares(squareList)
        self.labelText.set("Welcome! Click a square to set the starting \
point.")

    def resetInstructions(self):
        """Brings step back to 1."""
        global step
        step = 1

if __name__ == '__main__':
    root = tk.Tk()
    app = Interface(master=root)
    app.master.title("AStar")
    app.mainloop()
