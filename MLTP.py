# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 
from tkinter import font
import numpy as np
from PIL import *
import copy
import math

# Organize into different Modes 
# add animations for bug splat 
# add animations for bug hit 
# add randomized bug generation 
# add timer to determine when the round is over 
# figure out gimp
# figure out level up


#bonus 
#add color when the shape is almost detected 

####################################
# Helper Functions 
####################################
def almostEqual(a1,a2):
    return abs(a1-a2) < 10**(-7)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# taken from http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def make2dList(rows, cols):
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

#taken from http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
####################################
# File IO 
####################################
def updateTrainingData(path,data):
    old = readFile(path)
    writeFile(path, old + str(data.trainingData))

def updateTypeData(path,data):
    old = readFile(path)
    content = format(old)
    old.append(data.trainingDataType)
    writeFile(path, old)

# [array([0, 0, 0, ..., 0, 0, 0])]
def format(s):
    new = s[1:len(s)-1]
    return new

def getTrainingData(path,data):
    pass

print(format("[array([0, 0, 0, ..., 0, 0, 0]),array([0, 0, 0, ..., 0, 0, 0]), array([0, 0, 0, ..., 0, 0, 0])]"))
####################################
# Testing Data
####################################
def fillGaps(board,pointsL):
    newBoard = copy.deepcopy(board)
    missedPoints = []
    for i in range(len(pointsL) - 1):
        T1 = pointsL[i]
        T2 = pointsL[i + 1]
        new = findInterlinkingDots(T1,T2)
        missedPoints.extend(copy.copy(new))

    for oldPoint in pointsL:
        x = oldPoint[0]
        y = oldPoint[1]
        newBoard[x][y] = 1

    for newPoint in missedPoints:
        x = newPoint[0]
        y = newPoint[1]
        newBoard[x][y] = 1
    return newBoard

def findF(T1,T2):
    x1,y1 = T1[0],T1[1]
    x2,y2 = T2[0],T2[1]
    if x1 == x2:
    # this is a vertical line 
        return None  
    k = (y1 - y2)/(x1 - x2)
    b = y1 - k*x1
    return (k,b)

def findInterlinkingDots(T1,T2):
    x1,y1 = T1[0],T1[1]
    x2,y2 = T2[0],T2[1]
    result = []
    if findF((x1,y1),(x2,y2)) == None:
        yStart = min(y1,y2)
        yStop = y1 + y2 - yStart
        for y in range(yStart + 1,yStop):
            result.append((x1,y))
    else:
        k,b = findF((x1,y1),(x2,y2))
        xStart = min(x1,x2) 
        xStop = x1 + x2 - xStart
        for x in range(xStart + 1,xStop):
            y = k*x + b 
            y = int(y)
            result.append((x,y))
    return result 

def flatten(L):
    new = []
    for subL in L:
        new.extend(subL)
    return tuple(new)

def specialDist(L1,L2):
    sum = 0
    if (len(L1) != len(L2)):
        print("two uneven lengths")
    for i in range(0,len(L1)):
        num1 = L1[i]
        num2 = L2[i]
        delta = abs(num1 - num2)
        sum += (delta)
    return math.sqrt(sum) 

def getType(L,data):
    k = 1
    #the number of neighbors we are comparing to 
    neighbors = getkNearestNeighbors(k,L,data.trainingData,data.trainingDataType)
    print("neighbors",neighbors)
    result = getVotes(neighbors)
    return result 

def getVotes(neighbors):
    hiType = None
    hiCount = 0
    for key in neighbors:
        curCount = neighbors[key]
        if (curCount > hiCount):
            hiType = key
            hiCount = curCount
    return hiType

def getkNearestNeighbors(k,L,dataL,typeL):
    neighbors = dict()
    distL = getDists(L,dataL)
    sortedDistL = sorted(distL)
    for i in range(k):
    #loop through the closest k neighbors
        neighbor = typeL[distL.index(sortedDistL[i])]
        print("neighbor:",neighbor,"dist",sortedDistL[i])
        if neighbor not in neighbors:
            neighbors[neighbor] = 1
        else:
            neighbors[neighbor] += 1
    return neighbors 

def getDists(L,dataL):
    distL = []
    for knownImg in dataL:
        dist = specialDist(L,knownImg)
        distL.append(dist)
    return distL

print(getkNearestNeighbors(3,[0,0,0],[[1,1,1],[0,0,0],[2,2,2],[0,0,0],[0,0,0]],["dog","dog","dog","cat","dog"]))
####################################
# Main(playMode)
####################################

def init(data):
    data.mode = "imputDataMode"
    data.doodle = []
    data.trainingData = []
    data.trainingDataType = []
    data.doodleBoard = make2dList(data.width,data.height)

def mousePressed(event, data):
    # use event.x and event.y
    # print("numpA:",numpA)
    data.doodle = []
    # this is used to draw 
    # # reset the new doodle 
    data.prevX = event.x
    data.prevY = event.y


def mouseDragged(canvas,event, data):
    # data.doodleBoard[event.x][event.y] = 1
    data.doodle.append((event.x,event.y))

def mouseReleased(event, data):
    board = fillGaps(data.doodleBoard,data.doodle)
    flattenedBoard= flatten(board)
    numpA = np.array(flattenedBoard)
    if data.mode == "imputDataMode":
        data.trainingData.append(numpA)
        print("training:",data.trainingData)
    elif data.mode == "classifyMode":
        data.input = numpA

    data.doodleBoard = make2dList(data.width,data.height)
    # reset the new board
    # this is used to store the data 

def keyPressed(event, data):
    if data.mode == "imputDataMode":
        imputDataModeKeyPressed(event, data)
    if data.mode == "classifyMode":
        classifyModeKeyPressed(event, data)

def imputDataModeKeyPressed(event, data):
    if event.keysym == "Down":
    #changing modes
        data.mode = "classifyMode"
    # elif event.keysym == "space":
    #     updateTrainingData("trainingData.txt",data)
    else:
    #the key is a type 
        if event.keysym == "n":
            imputType = "n"
        elif event.keysym == "v":
            imputType = "v"
        elif event.keysym == "b":
            imputType = "verticalBar"
        elif event.keysym == "l":
            imputType = "horizontalLine"
        data.trainingDataType.append(imputType)
    print("types:",data.trainingDataType)

def classifyModeKeyPressed(event, data):
    if event.keysym == "space":
        print("The Result:",getType(data.input,data))
    

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.mode == "imputDataMode":
        canvas.create_text(200,200,text = "imputDataMode")
    elif data.mode == "classifyMode":
        canvas.create_text(200,200,text = "classifyMode")
    #draw the doodle
    if len(data.doodle) > 1:
        drawDoodle(canvas, data.doodle)

def drawDoodle(canvas, points):
    prevX,prevY = points[0][0],points[0][1]
    for (x,y) in points[1:]:
        canvas.create_line(prevX,prevY,x,y,width = 3)
        prevX,prevY = x,y

####################################
# Run 
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseReleasedWrapper(event, canvas, data):
        mouseReleased(event, data)
        redrawAllWrapper(canvas, data)

    def mouseDraggedWrapper(event, canvas, data):
    	mouseDragged(canvas,event, data)
    	redrawAllWrapper(canvas, data)
    
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
    	                    mouseDraggedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event:
                            mouseReleasedWrapper(event, canvas, data))
    
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 750)
#(4 by 3)
