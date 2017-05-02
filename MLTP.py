# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 
from tkinter import font
import numpy as np
from PIL import *
import copy
import math
import tkinter
import time
from sklearn import *
import pickle 
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
    for row in range(rows): a += [[1]*cols]
    return a

def distance(L1,L2):
    x1 = L1[0][0]
    x2 = L2[0][0]
    y1 = L1[0][1]
    y2 = L2[0][1]
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#taken from http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists

def cleanUp(L):
    result = []
    for shape in L:
        new = ''
        for i in range(1,len(shape)):
            c = shape[i]
            if not c =="\'" and not c =="\\":
                new = new + c 
        result.append(new)
    return result

####################################
# Training Data
####################################

def fillGaps1(pointsL):
    missedPoints = copy.deepcopy(pointsL)
    for i in range(len(pointsL) - 1):
        T1 = pointsL[i]
        T2 = pointsL[i + 1]
        new = findInterlinkingDots(T1,T2)
        missedPoints.extend(copy.copy(new))
    return sorted(missedPoints)

def fillGaps2(pointsL):
    # startTime = time.time()
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
        newBoard[x][y] = 2

    for newPoint in missedPoints:
        x = newPoint[0]
        y = newPoint[1]
        newBoard[x][y] = 2
    # endTime = time.time()
    # print("fillGaps took %f seconds" % (endTime - startTime))
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
    return new

def getRelativePosition(doodle):
    print("doodle",doodle)
    x1,y1 = doodle[0][0],doodle[0][1]
    x3,y3 = doodle[2][0],doodle[2][1]
    fullDoodle = fillGaps1(doodle)
    x2 = (x1 + x3)//2
    for dot in fullDoodle:
        if dot[0] == x2:
            y2 = dot[1]
    denominator = (x3-x1) 
    if denominator == 0:
        denominator = 0.1
    scale = 4
    delta1 = scale* (y2 - y1)/denominator
    delta2 = scale* (y3 - y1)/denominator
    return([delta1,delta2])



def specialDist(L1,L2):
    sum = 0
    print("new:",L1,"known:",L2)
    if ((np.count_nonzero(L1)) != (np.count_nonzero(L2))):
        print("two uneven lengths(specialDist)")
    print("len",np.count_nonzero(L1))
    for i in range(0,np.count_nonzero(L1)):
        num1 = L1[0][i]
        num2 = L2[0][i]
        delta = abs(num1 - num2)
        sum += (delta)
    return math.sqrt(sum) 

def getType(new,data):
    k = 1
    #the number of neighbors we are comparing to 
    neighbors = getkNearestNeighbors(k,new,data.transformedTrainingData,data.trainingDataType)
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

def getkNearestNeighbors(k,new,dataL,typeL):
    if ((np.count_nonzero(dataL)) != (np.count_nonzero(typeL))):
        print("two uneven lengths(trainingList, trainingTypeList)")
    neighbors = dict()
    distL = getDists(new,dataL)
    sortedDistL = np.sort(distL)
    for i in range(k):
    #loop through the closest k neighbors
        itemindexes = np.where(distL==sortedDistL[i])
        index = itemindexes[0][0]
        neighbor = typeL[index]
        print("neighbor:",neighbor,"dist",sortedDistL[i])
        if neighbor not in neighbors:
            neighbors[neighbor] = 1
        else:
            neighbors[neighbor] += 1
    return neighbors 

def getDists(new,dataL):
    distL = np.asarray([])
    for knownImg in (dataL):
        dist = distance(new,knownImg)
        distL = np.append(distL,dist)
    return distL

def getPCA(L):
    #builds a pca model that serves as a black box
    #takes in a flattened list and returns a tuple of length 2
    pca = decomposition.PCA(n_components=2)
    pca.fit(L)
    return pca 
#taken from https://www.youtube.com/watch?v=SBYdqlLgbGk

def getPCATransformedData(L,newPCA,data):
    #This returns transformed training data  
    result = []
    for img in data.trainingData:
        result.append(newPCA.transform(img))
    return result 

####################################
# Main(playMode)
####################################

def init(data):
    data.mode = "imputDataMode"
    data.doodle = []
    data.trainingData = np.loadtxt("trainingData.txt","int")
    if len(data.trainingData) == 0:
        data.trainingData = np.empty((0, 2),dtype=int)
    #at the very beggining, the file starts out empty
    #the file is read as np.asarray([])
    #so data.trainingData is always a ndarray
    data.trainingDataType = np.loadtxt("trainingDataType.txt",'str')
    data.trainingDataType = np.array(data.trainingDataType).tolist()
    data.trainingDataType  = cleanUp(data.trainingDataType)

    if len(data.trainingDataType) == 0:
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
    relativePosition = getRelativePosition(data.doodle)
    numpA = np.asarray(relativePosition)

    if data.mode == "imputDataMode":
        data.trainingData = np.append(data.trainingData,[numpA],axis=0)
    elif data.mode == "classifyMode":
        data.input = numpA
    print("trainingData",data.trainingData)

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
        #save the thing to the txt file automatically when the rest is done 
        # np.savetxt("trainingData.txt",data.trainingData, fmt="%d")
        np.savetxt("trainingDataType.txt",data.trainingDataType, fmt = "%s")
    elif event.keysym == "space":
        data.newPCA = getPCA(data.trainingData)
        newPCAFile = open("myPCAModel.p","wb")
        pickle.dump(data.newPCA,newPCAFile)
        newPCAFile.close()
        
        data.transformedTrainingData = getPCATransformedData(data.trainingData,data.newPCA,data)
        print("transformed!",data.transformedTrainingData)
        newTrainingDataFile = open("myNewTrainingData.p","wb")
        pickle.dump(data.transformedTrainingData,newTrainingDataFile)
        newTrainingDataFile.close()
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

def classifyModeKeyPressed(event, data):
    if event.keysym == "space":
        newInput = data.newPCA.transform(data.input)
        print("The Result:",getType(newInput,data))
    
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