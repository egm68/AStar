import random
from random import randint
from queue import LifoQueue
import matplotlib.pyplot as plt

print('Executing Gridworld Generator\n')

# Constant parameters for gridworld generation
NUM_OF_GRIDWORLDS = 50
PROB_OF_BLOCKED = 0.3
NUM_OF_ROWS = 10
NUM_OF_COLS = 10

"""
Each position in the gridworld is represented by a Cell. A Cell can be either 
visited or blocked. Initially, each cell in the gridworld is set as unvisited.
"""
class Cell:
    visited = False
    blocked = None

"""
Determines if a Cell is set as blocked or unblocked.
Returns True with probability, PROB_OF_BLOCKED. (Cell blocked)
Returns False with probability, 1 - PROB_OF_BLOCKED. (Cell unblocked)
"""
def isBlocked():
    if (random.random() < PROB_OF_BLOCKED):
        return True
    else:
        return False

"""
Generates the string form of a set of indicies.
row is the x coordinate, and col is the y coordinate.
Returns the string form of the indicies. (XrowYcol)
"""
def createIndices(row, col):
    return "X" + str(row) + "Y" + str(col)

"""
Isolates the row and col from the string form of a pair of indicies.
position is the string form of the indicies. (XrowYcol)
Returns the row and col.
"""
def getIndices(position):
    xIndex = position.index('X')
    yIndex = position.index('Y')
    row = int(position[xIndex + 1:yIndex])
    col = int(position[yIndex + 1:])
    return row, col

"""
Generates a single gridworld environment in the form of a matrix.
Each element in the matrix contains a Cell object.
Returns the gridworld as well as a list of all Cells that're unblocked. 
"""
def generateGridworld():

    # Initializes the gridworld and visited queue
    gridworld = [[Cell() for i in range(NUM_OF_COLS)] for j in range(NUM_OF_ROWS)]
    visited = LifoQueue()

    unvisited = []
    unblocked = []

    # Adds every Cell to the unvisited list and unblocked list
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLS):
            unvisited.append(createIndices(row, col))
            unblocked.append(createIndices(row, col))

    # Randomly chooses the starting row and column
    row = randint(0, NUM_OF_ROWS - 1)
    col = randint(0, NUM_OF_COLS - 1)

    allCellsVisited = False

    while not allCellsVisited:
        # Appends position of current cell to visited queue
        visited.put(createIndices(row, col))

        if (not gridworld[row][col].visited):
            unvisited.remove(createIndices(row, col))

        # Sets the current cell to visited and unblocked
        gridworld[row][col].visited = True
        gridworld[row][col].blocked = False

        # List of options for next movement 
        # 0: North, 1: East, 2: South, 3: West
        directions = [0, 1, 2, 3]
        nextMovement = random.choice(directions)
        findingUnvisited = True

        while findingUnvisited:

            # Next movement is North and North Cell is accessible
            if (nextMovement == 0 and row - 1 >= 0 and gridworld[row - 1][col].visited == False and gridworld[row - 1][col].blocked != True):
                if (isBlocked()):
                    gridworld[row - 1][col].blocked = True
                    unvisited.remove(createIndices(row - 1, col))
                    unblocked.remove(createIndices(row - 1, col))
                else:
                    gridworld[row - 1][col].blocked = False
                    findingUnvisited = False
                    row = row - 1

            # Next movement is East and East Cell is accessible
            elif (nextMovement == 1 and col + 1 <= NUM_OF_COLS - 1 and gridworld[row][col + 1].visited == False and gridworld[row][col + 1].blocked != True):
                if (isBlocked()):
                    gridworld[row][col + 1].blocked = True
                    unvisited.remove(createIndices(row, col + 1))
                    unblocked.remove(createIndices(row, col + 1))
                else:
                    gridworld[row][col + 1].blocked = False
                    findingUnvisited = False
                    col = col + 1

            # Next movement is South and South Cell is accessible
            elif (nextMovement == 2 and row + 1 <= NUM_OF_ROWS - 1 and gridworld[row + 1][col].visited == False and gridworld[row + 1][col].blocked != True):
                if (isBlocked()):
                    gridworld[row + 1][col].blocked = True
                    unvisited.remove(createIndices(row + 1, col))
                    unblocked.remove(createIndices(row + 1, col))
                else:
                    gridworld[row + 1][col].blocked = False
                    findingUnvisited = False
                    row = row + 1

            # Next movement is West and West Cell is accessible
            elif (nextMovement == 3 and col - 1 >= 0 and gridworld[row][col - 1].visited == False and gridworld[row][col - 1].blocked != True):
                if (isBlocked()):
                    gridworld[row][col - 1].blocked = True
                    unvisited.remove(createIndices(row, col - 1))
                    unblocked.remove(createIndices(row, col - 1))
                else:
                    gridworld[row][col - 1].blocked = False
                    findingUnvisited = False
                    col = col - 1
            
            # Unable to make current move because the Cell is unaccessible
            else: 
                directions.remove(nextMovement)

                if not directions: # No remaining movement options
                    findingUnvisited = False
                    visited.get()
                    
                    if visited.empty(): # No Cells to backtrack to
                        if (len(unvisited) == 0): 
                            # All Cells have been visited
                            allCellsVisited = True
                        else: 
                            # Randomly choose an unvisited Cell to start from
                            newUnvisitedCell = random.choice(unvisited)
                            row, col = getIndices(newUnvisitedCell)
                    else: 
                        # Backtrack to previous Cell
                        parent = visited.get()
                        row, col = getIndices(parent)
                else: # At least one more movement option
                    nextMovement = random.choice(directions)


    #gridworld = [[Cell() for i in range(6)] for j in range(6)]

    #gridworld[0][0].blocked = False
    #gridworld[0][1].blocked = False
    #gridworld[0][2].blocked = False
    #gridworld[0][3].blocked = False
    #gridworld[0][4].blocked = False
    #gridworld[0][5].blocked = False
    
    #gridworld[1][0].blocked = False
    #gridworld[1][1].blocked = True
    #gridworld[1][2].blocked = True
    #gridworld[1][3].blocked = False
    #gridworld[1][4].blocked = True
    #gridworld[1][5].blocked = True
    
    #gridworld[2][0].blocked = False
    #gridworld[2][1].blocked = False
    #gridworld[2][2].blocked = True
    #gridworld[2][3].blocked = False
    #gridworld[2][4].blocked = False
    #gridworld[2][5].blocked = True

    #gridworld[3][0].blocked = False
    #gridworld[3][1].blocked = False
    #gridworld[3][2].blocked = True
    #gridworld[3][3].blocked = True
    #gridworld[3][4].blocked = True
    #gridworld[3][5].blocked = True

    #gridworld[4][0].blocked = False
    #gridworld[4][1].blocked = False
    #gridworld[4][2].blocked = False
    #gridworld[4][3].blocked = False
    #gridworld[4][4].blocked = True
    #gridworld[4][5].blocked = False

    #gridworld[5][0].blocked = False
    #gridworld[5][1].blocked = False
    #gridworld[5][2].blocked = False
    #gridworld[5][3].blocked = True
    #gridworld[5][4].blocked = False
    #gridworld[5][5].blocked = True

    return gridworld, unblocked