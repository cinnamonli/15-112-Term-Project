from tkinter import *
import random 
from tkinter import font
import PIL
from PIL import Image, ImageOps
from PIL import ImageTk
from PIL import *
import math
import numpy as np
import pickle 
import copy
import time
from sklearn import *

####################################
# Helper Functions 
####################################
def almostEqual(a1,a2):
    return abs(a1-a2) < 10**(-7)
    
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
    #This is a feature that is unafffected by absolute position
    n = len(doodle)
    k = 4
    m = 3
    index1 = 0
    index2 = n//k
    index3 = n//2
    index4 = n * m//k
    index5 = -1
    x1,y1 = doodle[index1][0],doodle[index1][1]
    x2,y2 = doodle[index2][0],doodle[index2][1]
    x3,y3 = doodle[index3][0],doodle[index3][1]
    x4,y4 = doodle[index4][0],doodle[index4][1]
    x5,y5 = doodle[index5][0],doodle[index5][1]
    print([(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5)])
    
    denominator1 = abs(x2-x1)
    if denominator1 == 0:
        denominator1 = 1
    denominator2 = abs(x3-x2)
    if denominator2 == 0:
        denominator2 = 1
    denominator3 = abs(x4-x3)
    if denominator3 == 0:
        denominator3 = 1
    denominator4 = abs(x5-x4)
    if denominator3 == 0:
        denominator3 = 1
    scale = 4
    #This is used to blow up the differences 
    delta1 = scale* (y2 - y1)/denominator1
    delta2 = scale* (y3 - y2)/denominator2
    delta3 = scale* (y4 - y3)/denominator3
    delta4 = scale* (y5 - y4)/denominator4
    return([delta1,delta2,delta3,delta4])


def specialDist(L1,L2):
    sum = 0
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

#################################################
# Buttons
#################################################

class Button(object):
    def __init__(self,x,y,ImgFile):
        self.x = x
        self.y = y
        self.img = ImgFile
        self.width, self.height = self.img.size

    def draw(self,canvas,data):
        TkFormat = PIL.ImageTk.PhotoImage(self.img)
        self.newImg = TkFormat
        #this stores the new image so it doesn't get garbage collected 
        canvas.create_image(self.x, self.y, image=self.newImg)

    def redirect(self,event,data):
        if ((event.x < self.x + self.width/2 and event.x > self.x - self.width/2)
            and (event.y < self.y + self.height/2 and event.y > self.y - self.height/2)):
            self.isPressed = True
            if data.mode == "mainScreenMode" and self.img == data.playButtonImg:
            #play is pressed
                data.mode = "playMode"
            elif data.mode == "mainScreenMode" and self.img == data.helpButtonImg:
            #help is pressed
                data.mode = "helperScreenMode" 
            elif data.mode == "mainScreenMode" and self.img == data.calibrateButtonImg:
            #train is pressed
                data.mode = "inputDataMode"    
            elif data.mode == "helperScreenMode" and self.img == data.backButtonImg:
                data.mode = "mainScreenMode" 
            elif data.mode == "inputDataMode" and self.img == data.backButtonImg:
                data.mode = "mainScreenMode"
            elif data.mode == "gameOverMode" and self.img == data.replayButtonImg:
                data.mode = "mainScreenMode"

#################################################
# Init
#################################################
def init(data):
    data.mode = "mainScreenMode"
    mainScreenModeInit(data)
    helperScreenModeInit(data)
    playModeInit(data)
    inputDataModeInit(data)

def loadButtons(data):
    data.playButtonImg = Image.open("playbutton.gif")
    data.helpButtonImg = Image.open("helpbutton.gif")
    data.replayButtonImg = Image.open("replaybutton.gif")
    data.backButtonImg = Image.open("backbutton.gif")
    data.calibrateButtonImg = Image.open("calibratebutton.gif")
    #Buttons created from 

def loadBackgrounds(data):
    data.mainBackgroundImg = Image.open("mainbackground.gif")
    # adapted from https://www.iconfinder.com/icons/310934/compose_draw_graph_line_pencil_write_icon
    data.backgroundImg1 = Image.open("background1.gif")
    data.backgroundImg2 = Image.open("background2.gif")
    data.backgroundImg3 = Image.open("background3.gif")
    data.gridBackgroundImg = Image.open("gridbackground.gif")

def mainScreenModeInit(data):
    #main screen button 
    loadButtons(data)
    loadBackgrounds(data)
    data.mplayButtonPressed = False
    data.mhelpButtonPressed = False
    data.mbuttons = [Button(data.width//3,data.height*2//3,data.playButtonImg),
    Button(data.width*2//3,data.height*2//3,data.helpButtonImg),
    Button(data.width//2,data.height*4//5,data.calibrateButtonImg)]

def helperScreenModeInit(data):
    #initializes everything in helperScreen mode
    data.hbackButtonPressed = False
    data.hbuttons = [Button(data.width*4//5,data.height*8//9,data.backButtonImg)]


def playModeInit(data):
    data.paused = False

def gameOverModeInit(data):
    data.gbuttons = [Button(data.width//2,data.height*4//5,data.replayButtonImg)]

def inputDataModeInit(data):
    #initializes everything used in "inputDataMode"
    data.ibackButtonPressed = False
    data.ibuttons = [Button(data.width*4//5,data.height*8//9,data.backButtonImg)]
    data.doodle = []
    data.trainingData = np.loadtxt("trainingData.txt","int")
    if len(data.trainingData) == 0:
        data.trainingData = np.empty((0, 4),dtype=float)
    #at the very beggining, the file starts out empty
    #the file is read as np.asarray([])
    #so data.trainingData is always a ndarray
    data.trainingDataType = np.loadtxt("trainingDataType.txt",'str')
    data.trainingDataType = np.array(data.trainingDataType).tolist()
    data.trainingDataType  = cleanUp(data.trainingDataType)

    if len(data.trainingDataType) == 0:
       data.trainingDataType = []
    data.doodleBoard = make2dList(data.width,data.height)

#################################################
# MousePressed
#################################################
def mousePressed(event, data):
    if data.mode == "mainScreenMode":
        mainScreenModeMousePressed(event,data)
    elif data.mode == "helperScreenMode":
        helperModeMousePressed(event,data)
    elif data.mode == "playMode":
        playModeMousePressed(event,data)
    elif data.mode == "inputDataMode":
        inputDataModeMousePressed(event,data)
    elif data.mode == "gameOverMode":
        gameOverModeMousePressed(event,data)
        
        

def mainScreenModeMousePressed(event,data):
    for button in data.mbuttons:
        button.redirect(event,data)
    

def helperModeMousePressed(event,data):
    for button in data.hbuttons:
        button.redirect(event,data) 

def playModeMousePressed(event,data):
    pass

def inputDataModeMousePressed(event,data):
    for button in data.ibuttons:
        button.redirect(event,data) 
    data.doodle = []
    # this is used to draw 
    # # reset the new doodle 
    data.prevX = event.x
    data.prevY = event.y

def gameOverModeMousePressed(event,data):
    pass

#################################################
# MouseDragged
#################################################

def mouseDragged(canvas,event, data):
    # data.doodleBoard[event.x][event.y] = 1
    data.doodle.append((event.x,event.y))

#################################################
# MouseReleased
#################################################

def mouseReleased(event, data):
    if data.mode == "playMode":
        playModeMouseReleased(event, data)
    elif data.mode == "inputDataMode":
        inputDataModeMouseReleased(event, data)

def playModeMouseReleased(event, data):
    pass

def inputDataModeMouseReleased(event, data):
    relativePosition = getRelativePosition(data.doodle)
    numpA = np.asarray(relativePosition)

    if data.mode == "imputDataMode":
        data.trainingData = np.append(data.trainingData,[numpA],axis=0)
    elif data.mode == "classifyMode":
        data.input = numpA

    data.doodleBoard = make2dList(data.width,data.height)
    # reset the new board
    # this is used to store the data 

#################################################
# KeyPressed
#################################################

def keyPressed(event, data):
    if data.mode == "mainScreenMode":
        mainScreenModeKeyPressed(event,data)
    elif data.mode == "helperScreenMode":
        helperScreenModeKeyPressed(event,data)
    elif data.mode == "playMode":
        playModeKeyPressed(event,data)
    elif data.mode == "inputDataMode":
        inputDataModeKeyPressed(event,data)
    elif data.mode == "gameOverMode":
        gameOverModeKeyPressed(event,data)

def mainScreenModeKeyPressed(event,data):
    pass

def helperScreenModeKeyPressed(event,data):
    pass

def playModeKeyPressed(event,data):
    pass

def inputDataModeKeyPressed(event,data):
    if event.keysym == "space":
        #save model to pickle file
        data.newPCA = getPCA(data.trainingData)
        newPCAFile = open("myPCAModel.p","wb")
        pickle.dump(data.newPCA,newPCAFile)
        newPCAFile.close()
        
        data.transformedTrainingData = getPCATransformedData(data.trainingData,data.newPCA,data)
        print("transformed!",data.transformedTrainingData)
        newTrainingDataFile = open("myNewTrainingData.p","wb")
        pickle.dump(data.transformedTrainingData,newTrainingDataFile)
        newTrainingDataFile.close()
        
        #save lists to txt file
        np.savetxt("trainingData.txt",data.trainingData, fmt="%d")
        np.savetxt("trainingDataType.txt",data.trainingDataType, fmt = "%s")

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
        elif event.keysym == "t":
            imputType = "thunder"
        data.trainingDataType.append(imputType)
        
def gameOverModeKeyPressed(event,data):
    pass

#################################################
# TimerFired
#################################################

def timerFired(data):
    print(data.mode)
    if data.mode == "mainScreenMode":
        mainScreenModeTimerFired(data)
    elif data.mode == "helperScreenMode":
        helperScreenModeTimerFired(data)
    elif data.mode == "playMode":
        playModeTimerFired(data)
    elif data.mode == "inputDataMode":
        inputDataModeTimerFired(data)
    elif data.mode == "gameOverMode":
        gameOverModeTimerFired(data)

def mainScreenModeTimerFired(data):
    pass

def helperScreenModeTimerFired(data):
    pass

def playModeTimerFired(data):
    pass

def inputDataModeTimerFired(data):
    pass

def gameOverModeTimerFired(data):
    pass

#################################################
# Draw
#################################################

def redrawAll(canvas, data):
    if data.mode == "mainScreenMode":
        mainScreenModeDraw(canvas,data)
    elif data.mode == "helperScreenMode":
        helperScreenModeDraw(canvas,data)
    elif data.mode == "playMode":
        playModeDraw(canvas,data)
    elif data.mode == "inputDataMode":
        inputDataModeDraw(canvas,data)
    elif data.mode == "gameOverMode":
        gameOverModeDraw(canvas,data)
        
def mainScreenModeDraw(canvas,data):
    TkFormat = PIL.ImageTk.PhotoImage(data.mainBackgroundImg)
    data.newImg = TkFormat
    #this stores the new image so it doesn't get garbage collected 
    canvas.create_image(data.width/2, data.height/2,image=data.newImg)
    for button in data.mbuttons:
        button.draw(canvas,data)
    Arcade190 = font.Font(family='ArcadeClassic',
        size=190, weight='bold')
    canvas.create_text(data.width/2, data.height/3,text="draw",font = Arcade190)

def helperScreenModeDraw(canvas,data):
    TkFormat = PIL.ImageTk.PhotoImage(data.gridBackgroundImg)
    data.newImg = TkFormat
    #this stores the new image so it doesn't get garbage collected 
    canvas.create_image(data.width/2, data.height/2,image=data.newImg)
    Arcade90 = font.Font(family='ArcadeClassic',
        size=90, weight='bold')
    canvas.create_text(data.width/2, data.height/9,text="instructions",font = Arcade90)
    for button in data.hbuttons:
        button.draw(canvas,data) 
def playModeDraw(canvas,data):
    pass

def inputDataModeDraw(canvas,data):
    margin = 50
    TkFormat = PIL.ImageTk.PhotoImage(data.gridBackgroundImg)
    data.newImg = TkFormat
    #this stores the new image so it doesn't get garbage collected 
    canvas.create_image(data.width/2, data.height/2,image=data.newImg)
    for button in data.ibuttons:
        button.draw(canvas,data)
    text1 = "Draw shapes and press the corresponding key for that drawing"
    text2 = """
    'b' = verical bar
    'l' = horizontal line
    'v' = v
    'n' = n
    't' = lightning bolt
    """
    text3 = "press space to save"
    Cambria30 = font.Font(family='Cambria',
        size=30, weight='bold')
    Cambria20 = font.Font(family='Cambria',
        size=20, weight='bold')
    canvas.create_text(data.width//2,margin,anchor = N, font = Cambria30,text = text1)
    canvas.create_text(margin,margin*2,anchor = NW, font = Cambria20,text = text2)
    canvas.create_text(data.width/2,data.height*8//9, font = Cambria30,text = text3)

    if len(data.doodle) > 1:
        drawDoodle(canvas, data.doodle)

def drawDoodle(canvas, points):
    prevX,prevY = points[0][0],points[0][1]
    for (x,y) in points[1:]:
        canvas.create_line(prevX,prevY,x,y,width = 3)
        prevX,prevY = x,y

def gameOverModeDraw(canvas,data):
    #add background
    for button in data.gbuttons:
        button.draw(canvas,data)
####################################
# use the run function as-is
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

#################################################
# main
#################################################
def KillTheBugs():
    run(1000, 750)

KillTheBugs()
