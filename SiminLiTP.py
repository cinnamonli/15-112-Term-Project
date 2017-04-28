# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 
from tkinter import font
import PIL
from PIL import Image, ImageOps
from PIL import ImageTk
from PIL import *
# import ImageOps


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

####################################
# Plant 
####################################
class Plant(object):
    def __init__(self,data):
        self.r = 30
        self.x = data.width//2
        self.y = data.height//2
        self.level = 1
        self.lives = 5
        self.isDead = False

    def updateDeath(self):
        if self.lives <= 0:
            self.isDead = True
            data.gameOver = True
    def reduceLives(self,bugs):
        pass
    def draw(self,canvas,data):
        left = data.width / 2
        top = data.height / 2
        TkFormat = PIL.ImageTk.PhotoImage(data.PILplantImg)
        data.genPlantImage = TkFormat
        #this stores the new image so it doesn't get garbage collected 
        canvas.create_image(left, top, image=data.genPlantImage)

####################################
# Bug 
####################################
def flipped(img):
    #returns the image only flipped horizontally 
    return ImageOps.mirror(img)
    
class Bug(object):
    def __init__(self,data):
        startLocations = getBorders(data.width,data.height)
        (self.x,self.y) = random.choice(startLocations) 
        if self.x <= data.width // 2:
        # if it is on the left hand side 
        # the current direction is correct 
            self.direction = True 
        else:
        # it is on the right hand side and facing 
        # the wrong direction 
            self.direction = False
        self.r = 10
        self.isDead = False
        xDist = data.plant.x - self.x
        yDist = data.plant.y - self.y
        if data.plant.level == 1:
        #level 1 is easy and most bugs contain only 1 shape
            
            self.xSpeed = xDist / 150
            self.ySpeed = yDist / 150 
            if (random.randint(0,1) < 0.1):
                self.shapeNum = random.randint(1,3)
            else:
                self.shapeNum = 1
        #level 2 is easy and most bugs contain only 1 shape
        #level 3 is easy and most bugs contain only 1 shape
        #level 4 is easy and most bugs contain only 1 shape
        #level 5 is difficult and everybug contains 4-9 shapes 
        self.shapeVals = ["n","v","horizontalLine","verticalBar"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
        flea = data.fleaImg
        pillar = data.pillarImg 
        bugs = [flea,pillar]
        self.bugType = random.choice(bugs)

    def draw(self,canvas,data):
        left = self.x
        top = self.y
        if not self.direction:
            image = flipped(self.bugType)
            image = ImageTk.PhotoImage(image)
            self.genBugImage = image
        #this stores the new image so it doesn't get garbage collected 
        else: 
            image = ImageTk.PhotoImage(self.bugType)
            self.genBugImage = image
        canvas.create_image(left, top, anchor = NW, image=self.genBugImage)

    def drawShapes(self,canvas,data):
        text = ""
        for shape in self.shapesRemaining:
            if shape == "n":
                text += "  A" 
            elif shape == "v":
                text += "  v" 
            elif shape == "horizontalLine":
                text += "  -" 
            elif shape == "verticalBar":
                text += "  |"
            Astera = font.Font(family='ASTERA', size=20)
            print(text)
        canvas.create_text(self.x, self.y - 20,text = text,anchor = N,font = Astera)

    def splat(self,canvas):
        #creates an animation effect when the bug is splatted 
        #import image 
        pass

    def move(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

    def updateDeath(self,data):
        if almostEqual(self.x,data.plant.x) and almostEqual(self.y,data.plant.y):
        #the bug has reached the plant 
            self.isDead = True
            if data.plant.lives > 0:
                data.plant.lives -= 1
            if data.score > 0:
                data.score -= data.scoreUnit

        elif self.shapesRemaining == []:
            # splat(self,canvas)
            self.isDead = True
            #add animation of bug splat 

    def deleteShape(self,event,data):
        input = ""
        if event.keysym == "n":
            input = "n" 
        elif event.keysym == "v":
            input = "v" 
        elif event.keysym == "l":
            input = "horizontalLine"
        elif event.keysym == "b":
            input = "verticalBar"
        if self.shapesRemaining!= [] and input == self.shapesRemaining[0]:
        # lethal hit to bug successful
            data.score += data.scoreUnit
            #add this to score
            self.shapesRemaining.pop(0) 


def buildShapes(num, vals):
    #builds up the shapes that each bug contains 
    result = []
    for i in range(num):
        new = random.choice(vals)
        result.append(new)
    return result 


def getBorders(width,height):
    #returns a list of locations that are on the outer frame of the canvas 
    border = []
    xVals = [0, width]
    yVals = [0, height]
    for x in xVals:
        for y in range(0,height,10):
            border.append((x,y))
    for y in yVals:
       for x in range(0,width,10):
           border.append((x,y))
    return border

####################################
# Main(playMode)
####################################

def init(data):
    preloadImages(data)
    data.gameOver = False
    data.plant = Plant(data)
    data.doodle = []
    data.scoreUnit = 1
    initLevel(data)
    print(data.bugs[0].shapesRemaining)

def preloadImages(data):
    data.PILplantImg = Image.open("seed.gif")
    # data.plantImg = PhotoImage(file="seed.gif")
    data.fleaImg = Image.open("flea.gif")
    data.pillarImg = Image.open("pillar.gif")


def initLevel(data):
    data.timer = 0
    data.bugTimer = 0
    data.score = 0
    data.bugs = []
    data.bugs.append(Bug(data))
    data.bugCount = 1
    data.levelComplete = False


def mousePressed(event, data):
    # use event.x and event.y
    data.doodle = []
    data.prevX = event.x
    data.prevY = event.y

def mouseDragged(canvas,event, data):
    print("mouseDragged")
    data.doodle.append((event.x,event.y))

def keyPressed(event, data):
    # use event.char and event.keysym
    for bug in data.bugs:
        bug.deleteShape(event,data)
    print("shapesremaining",data.bugs[0].shapesRemaining)

def timerFired(data):
    millisecond = 1000
    data.timer += (data.timerDelay/millisecond) 
    data.bugTimer += (data.timerDelay/millisecond) 
    
    if data.plant.level == 1:
        #level 1 is easy and bugs appear less frequently     
        if data.bugTimer > 5 and data.bugCount < 25:
            if random.randint(0,1) > 0.5:
                data.bugs.append(Bug(data))
                data.bugTimer = 0
                data.bugCount += 1
        #level 2 is more difficult and bugs appear more frequently 
        #level 3 is difficult and bugs appear in swarms 
        #level 4 is hard and there are a lot of bugs in swarms 
        #level 5 is very hard and you must use special operators to win
    if data.bugs != []:
        for bug in data.bugs:
            if bug.isDead == False:
                bug.move()
                bug.updateDeath(data)
    if data.levelComplete == True:
        #transition Page 
        #move to next level 
        pass

def redrawAll(canvas, data):
    #draw the plant 
    data.plant.draw(canvas,data)

    #draw the bugs
    if data.bugs != []:
        for bug in data.bugs:
            if bug.isDead == False:
                bug.draw(canvas,data)
                bug.drawShapes(canvas,data)
    #draw the doodle
    if len(data.doodle) > 1:
        drawDoodle(canvas, data.doodle)
    
    #draw the score at top right
    drawScore(canvas,data)

    #draw the lives at top left 
    drawLives(canvas,data)

def drawDoodle(canvas, points):
    prevX,prevY = points[0][0],points[0][1]
    for (x,y) in points[1:]:
        canvas.create_line(prevX,prevY,x,y,width = 3)
        prevX,prevY = x,y

def drawScore(canvas,data):
    margin = 20
    text = str(data.score) 
    Arcade90 = font.Font(family='ArcadeClassic',
        size=90, weight='bold')
    canvas.create_text(data.width - 100, margin,text = text,anchor = NW, font = Arcade90)

def drawLives(canvas,data):
    #draws the remaining lives at top left
    margin = 40
    total = 5
    lives = data.plant.lives 
    lost = total - lives
    text = "* " * lives + "| " * lost 
    # in this special font "*" is a full heart 
    # "|" is an empty heart that represents life lost
    Heart40 = font.Font(family='My Big Heart Demo',
        size=40, weight='bold')
    canvas.create_text(margin //2, margin,text = text,anchor = NW, font = Heart40)

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
    data.timerDelay = 100 # milliseconds
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
