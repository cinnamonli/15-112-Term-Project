# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 
from tkinter import font
import numpy as np
from PIL import *
import copy

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
# Testing Data
####################################
def fillGaps(board,pointsL):
    newBoard = copy.deepcopy(board)
    missedPoints = []
    for i in range(len(pointsL) - 1):
        T1 = pointsL[i]
        T2 = pointsL[i + 1]
        new = findInterlinkingDots(T1,T2)
        print("start:", T1, "stop:", T2,"new:",new )
        missedPoints.extend(new)
    for point in missedPoints:
        x = point[0]
        y = point[1]
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

print(findInterlinkingDots((0,0),(5,5)))


####################################
# Main(playMode)
####################################

def init(data):
    data.doodle = []
    data.trainingData = []
    data.trainingDataType = []

def mousePressed(event, data):
    # use event.x and event.y
    data.doodle = []
    # reset the new doodle
    # this is used to draw 
    data.doodleBoard = make2dList(data.width,data.height)
    # reset the new board
    # this is used to store the data  
    data.prevX = event.x
    data.prevY = event.y
    board = fillGaps(data.doodleBoard,data.doodle)
    numpA = np.array(board)
    print("numpA:",numpA)


def mouseDragged(canvas,event, data):
    data.doodleBoard[event.x][event.y] = 1
    data.doodle.append((event.x,event.y))

def keyPressed(event, data):
    pass

def timerFired(data):
    print("doodle:",data.doodle)

def redrawAll(canvas, data):
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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 750)
#(4 by 3)
