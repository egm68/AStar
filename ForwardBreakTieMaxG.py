import random
import timeit
import heapq
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from ForwardBreakTieMinG import ForwardBreakTieMinG
from GridworldGenerator import generateGridworld
from GridworldGenerator import getIndices
from Backward import Backward
from Adaptive import AdaptiveMain

# custom heap comparison function (favors smaller g-values)
def new_cmp_lt_minG(self):
  global s_start
  global openList

  s_min = None
  f_min = float('inf')
  minFList = []
  minGList = []
  g_min = float('inf')

  for i in range(len(openList)):
    if openList[i].f_value < f_min:
      minFList.clear()
      minFList.append(openList[i])
      f_min = openList[i].f_value
    elif openList[i].f_value == f_min:
      minFList.append(openList[i])

  #IF NO TIES F_VALUE
  if len(minFList) == 1:
    s_min = minFList[0]
    f_min = minFList[0].f_value
  else:  
    #BREAKING F_VALUE TIES IN FAVOR OF CELLS WITH SMALLER G-VALUES (remaining ties broken randomly)
    for i in range(len(minFList)):
        if minFList[i].g_value < g_min:
            minGList.clear()
            minGList.append(minFList[i])
            g_min = minFList[i].g_value
        elif minFList[i].g_value == g_min:
            minGList.append(minFList[i]) 

    if (len(minGList) == 1):
        s_min = minGList[0]
        f_min = minGList[0].f_value 
    else:
        s_min = random.choice(minGList)
        f_min = s_min.f_value 

  return s_min

# Override the existing "cmp_lt" module function with our function
heapq.cmp_lt=new_cmp_lt_minG

# custom heap comparison function (favors larger g-values)
def new_cmp_lt_maxG(self):
  global s_start
  global openList

  s_min = None
  f_min = float('inf')
  minFList = []
  maxGList = []
  g_max = 0

  for i in range(len(openList)):
    if openList[i].f_value < f_min:
      minFList.clear()
      minFList.append(openList[i])
      f_min = openList[i].f_value
    elif openList[i].f_value == f_min:
      minFList.append(openList[i])

  #IF NO TIES F_VALUE
  if len(minFList) == 1:
    s_min = minFList[0]
    f_min = minFList[0].f_value
  else:  
    #BREAKING F_VALUE TIES IN FAVOR OF CELLS WITH LARGER G-VALUES (remaining ties broken randomly)
    for i in range(len(minFList)):
        if minFList[i].g_value > g_max:
            maxGList.clear()
            maxGList.append(minFList[i])
            g_max = minFList[i].g_value
        elif minFList[i].g_value == g_max:
            maxGList.append(minFList[i]) 

    if (len(maxGList) == 1):
        s_min = maxGList[0]
        f_min = maxGList[0].f_value 
    else:
        s_min = random.choice(maxGList)
        f_min = s_min.f_value 

  return s_min

def manhattanDist(row1, col1, row2, col2):
  return abs(row1 - row2) + abs(col1 - col2)

def addPathToPdf(path, pdf, startRow, startCol, endRow, endCol):
    # Inititalizes the plot where the gridworld will be visualized
    gw_plot = plt.gca()
    gw_plot.patch.set_facecolor('gray')
    gw_plot.set_aspect('equal', 'box')
    gw_plot.xaxis.set_major_locator(plt.NullLocator())
    gw_plot.yaxis.set_major_locator(plt.NullLocator())

    for i in range(len(S)):
        for j in range(len(S[0])):
            if (i == startRow and j == startCol):
                # Colors starting Cell blue
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='blue')
            elif (i == endRow and j == endCol):
                # Colors target Cell red
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='red')
            elif (S[i][j].blocked):
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='black')
            else:
                if ((i, j) in path):
                    # Colors unblocked Cells that are on the path green 
                    rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='green')
                else:
                    # Colors unblocked Cells that aren't on the path white
                    rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='white')

            # Adds colored Cell to gridworld plot
            gw_plot.add_patch(rect)

    # Formats the plot
    gw_plot.autoscale_view()
    figure = gw_plot.get_figure()
    pdf.savefig(figure)

    return pdf

def minInOpenListGMax():
  global s_start
  global openList

  s_min = None
  f_min = float('inf')
  minFList = []
  maxGList = []
  g_max = 0

  for i in range(len(openList)):
    if openList[i].f_value < f_min:
      minFList.clear()
      minFList.append(openList[i])
      f_min = openList[i].f_value
    elif openList[i].f_value == f_min:
      minFList.append(openList[i])

  #IF NO TIES F_VALUE
  if len(minFList) == 1:
    s_min = minFList[0]
    f_min = minFList[0].f_value
  else:  
    #BREAKING F_VALUE TIES IN FAVOR OF CELLS WITH LARGER G-VALUES (remaining ties broken randomly)
    for i in range(len(minFList)):
        if minFList[i].g_value > g_max:
            maxGList.clear()
            maxGList.append(minFList[i])
            g_max = minFList[i].g_value
        elif minFList[i].g_value == g_max:
            maxGList.append(minFList[i]) 

    if (len(maxGList) == 1):
        s_min = maxGList[0]
        f_min = maxGList[0].f_value 
    else:
        s_min = random.choice(maxGList)
        f_min = s_min.f_value 

  return s_min

def ComputePath(gridworld):
  global S
  global s_goal
  global s_start
  global openList
  global closedList
  global counter

  firstCell = True
  
  s_current = s_start

  while (s_goal.g_value > minInOpenListGMax().f_value):
        s_current = minInOpenListGMax()
        index = openList.index(s_current)
        openList.pop(index)
        closedList.append(s_current)

        for i in range(4):
            action = None
            if (i == 0):
                action = s_current.north
            elif (i == 1):
                action = s_current.east
            elif (i == 2):
                action = s_current.south
            else:
                action = s_current.west

            if action != None and firstCell:
                S[action.row][action.col].blocked = gridworld[action.row][action.col].blocked
                if (gridworld[action.row][action.col].blocked):
                    S[action.row][action.col].a_cost = float('inf')

            if action != None and action not in closedList:
                if action.search < counter:
                    action.g_value = float('inf')
                    action.search = counter
                if action.g_value > s_current.g_value + action.a_cost:

                    action.g_value = s_current.g_value + action.a_cost
                    action.tree = s_current

                    if (action in openList):
                        index = openList.index(action)
                        openList.pop(index)
                    
                    action.f_value = action.g_value + action.h_value
                    openList.append(action)

        firstCell = False
    
def ForwardBreakTieMaxG(gridworld, startRow, startCol, endRow, endCol, pdf):
    global S
    global s_start
    global s_goal
    global openList
    global closedList
    global counter
    global complete_path
    global final_path

    pdf = initialize(gridworld, startRow, startCol, endRow, endCol, pdf)

    counter = 0
    final_path.append(S[startRow][startCol])

    for i in range(len(S)):
        for j in range(len(S[0])):
            S[i][j].search = 0

    while (s_start.row != s_goal.row or s_start.col != s_goal.col):
        counter = counter + 1
        s_start.g_value = 0
        s_start.search = counter
        s_goal.g_value = float('inf')
        s_goal.search = counter
        openList.clear()
        closedList.clear()
        complete_path.clear()
        s_start.f_value = s_start.g_value + s_start.h_value
        openList.append(s_start)
        ComputePath(gridworld)
        if len(openList) == 0:
            print("I cannot reach the target.")
            break
        temp = s_goal
        complete_path.append(temp)
        while (temp.tree != s_start):
            complete_path.append(temp.tree)
            temp = temp.tree
        complete_path.append(s_start)
        complete_path.reverse()

        if (len(complete_path) > 1):
            s_start = complete_path[1]

            if (s_start in final_path):
              index = final_path.index(s_start)
              final_path = final_path[0: index]

            final_path.append(s_start)

        final_path_indices = []
        for s in final_path:
            final_path_indices.append((s.row, s.col))

        # Add path to plot pdf
        pdf = addPathToPdf(final_path_indices, pdf, startRow, startCol, endRow, endCol)

    if (s_start.row == s_goal.row and s_start.col == s_goal.col):
        print("I reached the target.")

    return pdf


def printCompletePath():
    global final_path

    print('Print complete path:')
    for s in final_path:
        print('[' + str(s.row) + ', ' + str(s.col) + ']')

def initialize(gridworld, startRow, startCol, endRow, endCol, pdf):
    global complete_path
    global final_path
    global closedList
    global openList
    global counter 
    global S 
    global s_start 
    global s_goal

    complete_path = [] 
    final_path = [] 
    closedList = [] 
    openList = [] 
    counter = 0 

    # Adds the actual gridworld with all blocked Cells, start goal, and end goal to PDF
    gw_plot = plt.gca()
    gw_plot.patch.set_facecolor('gray')
    gw_plot.set_aspect('equal', 'box')
    gw_plot.xaxis.set_major_locator(plt.NullLocator())
    gw_plot.yaxis.set_major_locator(plt.NullLocator())

    for i in range(len(gridworld)):
        for j in range(len(gridworld[0])):
            if (i == startRow and j == startCol):
                # Colors starting Cell blue
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='blue')
            elif (i == endRow and j == endCol):
                # Colors target Cell red
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='red')
            elif (gridworld[i][j].blocked):
                # Colors unblocked Cells black
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='black')
            else:
                # Colors unblocked Cells white
                rect = plt.Rectangle([i, j], 1, 1, edgecolor='black', facecolor='white')

            # Adds colored Cell to gridworld plot
            gw_plot.add_patch(rect)

    # Formats the plot
    gw_plot.autoscale_view()
    figure = gw_plot.get_figure()
    pdf.savefig(figure)

    # Initalizes all the Cells in gridworld
    S =  [[Cell() for i in range(len(gridworld))] for j in range(len(gridworld[0]))]

    # Sets default values for each Cell in gridworld
    for row in range(len(gridworld)):
        for col in range(len(gridworld[0])):
            S[row][col].blocked = False
            S[row][col].row = row
            S[row][col].col = col
            S[row][col].a_cost = 1
            S[row][col].h_value = manhattanDist(row, col, endRow, endCol)
            if (row == 0):
                S[row][col].north = None
            else:
                S[row][col].north = S[row - 1][col]

            if (col == 0):
                S[row][col].west = None
            else:
                S[row][col].west = S[row][col - 1]

            if (row == len(gridworld) - 1):
                S[row][col].south = None
            else:
                S[row][col].south = S[row + 1][col]

            if (col == len(gridworld[0]) - 1):
                S[row][col].east = None
            else:
                S[row][col].east = S[row][col + 1]

    s_start = S[startRow][startCol]
    s_goal = S[endRow][endCol]

    return pdf

class Cell:
    def __init__(self):
        # Indicates row and column of Cell
        self.row = None
        self.col = None

        # Current path
        self.tree = None

        # link to neighbors of Cell
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        # Additional data about Cell
        self.blocked = None
        self.f_value = None
        self.g_value = None
        self.h_value = None
        self.a_cost = None
        self.search = None

complete_path = None
final_path = None 
closedList = None
openList = None 
counter = None
startRow = None
startCol = None
endRow = None
endCol = None
S =  None
s_start = None
s_goal = None

forwardTimes = []
backwardTimes = []

# PDF that'll contain the paths computed by all the A* searches
pdf = matplotlib.backends.backend_pdf.PdfPages("ForwardBreakTieMaxG_Paths.pdf")

# Create gridworld
gridworld, unblocked = generateGridworld()

# Randomly choose the start Cell for gridworld
startingCell = random.choice(unblocked)
startRow, startCol = getIndices(startingCell)

unblocked.remove(startingCell)

# Randomly choose the goal Cell for gridworld
endCell = random.choice(unblocked)
endRow, endCol = getIndices(endCell)

start = timeit.default_timer()
pdf = ForwardBreakTieMaxG(gridworld, startRow, startCol, endRow, endCol, pdf)
stop = timeit.default_timer()

print("Runtime of ForwardBreakTieMaxG was " + str(stop - start))

# Close the PDF
pdf.close()
    


