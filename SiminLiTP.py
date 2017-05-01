# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 
from tkinter import font
import PIL
from PIL import Image, ImageOps
from PIL import ImageTk
from PIL import *
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
    return abs(a1-a2) < 20

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
#taken from http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
####################################
# Plant 
####################################
class Plant(object):
    def __init__(self,data):
        self.x = data.width//2
        self.y = (data.height - data.upperMargin)//2 + data.upperMargin
        self.level = 2
        self.lives = 5
        self.isDead = False

    def updateDeath(self):
        if self.lives < 0:
            self.isDead = True
            data.gameOver = True
        if data.gameOver == True:
            data.mode == "GameOverMode"

    def draw(self,canvas,data):
        centerX = self.x
        centerY = self.y
        TkFormat = PIL.ImageTk.PhotoImage(data.PILplantImg)
        data.genPlantImage = TkFormat
        #this stores the new image so it doesn't get garbage collected 
        canvas.create_image(centerX, centerY, image=data.genPlantImage)

####################################
# Bug 
####################################
def flipped(img):
    #returns the image only flipped horizontally 
    return ImageOps.mirror(img)
    
class Bug(object):
    def initLevel1Bug(self,data):
        slowRatio = 150
        fastRatio = 130
        hi = 3
        if (random.randint(0,1) < 0.1):
            self.shapeNum = random.randint(1,hi)
            self.xSpeed = self.xDist /slowRatio
            self.ySpeed = self.yDist /slowRatio 
        else:
            self.shapeNum = 1
            self.xSpeed = self.xDist /fastRatio
            self.ySpeed = self.yDist /fastRatio

    def initLevel2Bug(self,data):
        fastRatio = 70
        normalRatio = 140
        lo = 2
        hi = 4
        if data.bugCount < 18:
            self.shapeNum = random.randint(lo,hi)
            self.xSpeed = self.xDist / normalRatio
            self.ySpeed = self.yDist / normalRatio 

        elif data.bugCount >= 18:
            self.shapeNum = 1
            self.xSpeed = self.xDist / fastRatio
            self.ySpeed = self.yDist / fastRatio 
            
    def initLevel3Bug(self,data):
        self.xSpeed = self.xDist / 140
        self.ySpeed = self.yDist / 140 
        if (random.randint(0,1) < 0.6):
            self.shapeNum = random.randint(1,4)
        else:
            self.shapeNum = 1
    def initLevel4Bug(self,data):
        self.xSpeed = self.xDist / 140
        self.ySpeed = self.yDist / 140 
        if (random.randint(0,1) < 0.2):
            self.xSpeed = self.xDist / 100
            self.ySpeed = self.yDist / 100 
        if (random.randint(0,1) < 0.6):
            self.shapeNum = random.randint(1,4)
        else:
            self.shapeNum = 1
    def initLevel5Bug(self,data):
        self.xSpeed = self.xDist / 130
        self.ySpeed = self.yDist / 130 
        if (random.randint(0,1) < 0.4):
            self.xSpeed = self.xDist / 100
            self.ySpeed = self.yDist / 100 
        self.shapeNum = random.randint(3,6)

    def initBug(self,data):
        if data.plant.level == 1:
        #level 1 is easy and most bugs contain only 1 shape
            Bug.initLevel1Bug(self,data)
            
        elif data.plant.level == 2:
        #level 2 is easy and most bugs contain only 1 shape
        #bugs crawl a bit faster
            Bug.initLevel2Bug(self,data)
            
        elif data.plant.level == 3:
        #level 3 is harder and most bugs 1-4 shapes
        #bugs crawl a bit faster
            Bug.initLevel3Bug(self,data)
            
        elif data.plant.level == 4:
        #level 4 is harder and most bugs contain only 1 shape
        #bugs crawl a bit faster, some crawl really fast
            Bug.initLevel4Bug(self,data)
            
        elif data.plant.level == 5:
        #level 5 is difficult with all containing 3-5 shapes 
        #bugs crawl a bit faster, some crawl really fast
            Bug.initLevel5Bug(self,data)

    def __init__(self,data):
        startLocations = getBorders(data.width,data.height, data)
        (self.x,self.y) = random.choice(startLocations) 
        if (len(data.bugs) > 0 and 
            dist(self.x,self.y,data.bugs[-1].x,data.bugs[-1].y) < 100):
                (self.x,self.y) = random.choice(startLocations) 
        #This is so that bugs dont start off overlapping 
        if self.x <= data.width // 2:
        # if it is on the left hand side 
        # the current direction is correct 
            self.direction = True 
        else:
        # it is on the right hand side and facing 
        # the wrong direction 
            self.direction = False
        self.isDead = False
        self.xDist = data.plant.x - self.x
        self.yDist = data.plant.y - self.y 
        Bug.initBug(self,data)
        self.shapeVals = ["n","v","horizontalLine","verticalBar"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
        flea = data.fleaImg
        pillar = data.pillarImg 
        bugs = [flea,pillar]
        #choose a type of bug
        self.bugType = random.choice(bugs)
        self.reborn = False
        #This will not be used for general bugs, just bosses to reset the shapes 
        self.lives = 1

    def draw(self,canvas,data):
        centerX = self.x
        centerY = self.y
        if not self.direction:
            image = flipped(self.bugType)
            image = ImageTk.PhotoImage(image)
            self.genBugImage = image
        #this stores the new image so it doesn't get garbage collected 
        else: 
            image = ImageTk.PhotoImage(self.bugType)
            self.genBugImage = image
        canvas.create_image(centerX, centerY, image=self.genBugImage)

    def drawShapes(self,canvas,data):
        text = ""
        margin = 40
        for shape in self.shapesRemaining:
            if shape == "n":
                text += "  A" 
            elif shape == "v":
                text += "  v" 
            elif shape == "horizontalLine":
                text += "  -" 
            elif shape == "verticalBar":
                text += "  |"
        Astera = font.Font(family='ASTERA', size=23)
        #This font can create upside down "V"s which is "A"
        if not isinstance(self,Boss):
            canvas.create_text(self.x, self.y - margin,text = text,font= Astera)

        elif isinstance(self,Boss) and self.xSpeed <= 0:
            canvas.create_text(self.x, self.y - margin,text = text,font= Astera)

    def splat(self,canvas,data):
        #creates an animation effect at the bug's death
        centerX = self.x
        centerY = self.y
        if not self.direction:
            image = flipped(data.splatImg)
            image = ImageTk.PhotoImage(image)
            self.genBugImage = image
        #this stores the new image so it doesn't get garbage collected 
        else: 
            image = ImageTk.PhotoImage(data.splatImg)
            self.genBugImage = image
        canvas.create_image(centerX, centerY,image=self.genBugImage)

    def move(self,data):
        self.x += self.xSpeed
        self.y += self.ySpeed

    def updateDeath(self,data):
        if almostEqual(self.x,data.plant.x) and almostEqual(self.y,data.plant.y):
        #the bug has reached the plant 
            #In this case, the bug does not die
            #It is removed from the list
            currentBugIndex = data.bugs.index(self)
            data.bugs.pop(currentBugIndex)
            if data.plant.lives > 0:
                data.plant.lives -= 1
            if data.score > 0:
                data.score -= data.scoreUnit

        elif self.shapesRemaining == []:
            #In this case, the bug dies
            self.isDead = True
            #It is removed from the list
            currentBugIndex = data.bugs.index(self)
            data.bugs.pop(currentBugIndex)
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

class Boss(Bug):
    def moveBack(self,data):
        #move the thing back to the original spot 
        superFastRatio = 30
        if self.x < data.width:
            self.xSpeed = -data.xDist/superFastRatio
            self.ySpeed = -data.yDist/superFastRatio

    def move(self,data):
        fastRatio = 90
        mediumRatio = 100
        normalRatio = 110
        if self.x >= data.width:
            #The bug moves faster and faster
            if self.lives > 2:
                self.xSpeed = data.xDist/fastRatio
                self.ySpeed = data.yDist/fastRatio
            elif self.lives > 1:
                self.xSpeed = data.xDist/mediumRatio
                self.ySpeed = data.yDist/mediumRatio
            else:
                self.xSpeed = data.xDist/normalRatio
                self.ySpeed = data.yDist/normalRatio

        self.x += self.xSpeed
        self.y += self.ySpeed

    def updateDeath(self,data):
        if self.x >= data.width and self.reborn == False:
            self.reborn = True

        if (almostEqual(self.x,data.plant.x)and almostEqual(self.y,data.plant.y) 
        and self.lives > 0):
        #the bug has reached the plant 
            self.lives -= 1
            if data.plant.lives > 0:
                data.plant.lives -= 1
            if data.score > 0:
                data.score -= data.scoreUnit
            GrassHopper.moveBack(self,data)
            self.shapeVals = ["n","v","horizontalLine","verticalBar"]
            self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
            self.reborn = False

        elif self.shapesRemaining == [] and self.lives > 0:
        #increase the speed each time
            self.lives -= 1 
            GrassHopper.moveBack(self,data)
            self.shapeVals = ["n","v","horizontalLine","verticalBar"]
            self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
            self.reborn = False

        elif self.shapesRemaining == [] and self.lives <= 0:
            # splat(self,canvas)
            self.isDead = True
            data.bossDead = True
            #add animation of bug splat

class GrassHopper(Boss):
    def __init__(self,data):
        self.direction = True 
        self.lives = 2
        #This is the number of times each string of things need to be eliminated 
        ratio = (8/10)
        grassHopperX = data.width
        grassHopperY = data.height * ratio
        #starts at the same location at the right of the screen 
        (self.x,self.y) = (grassHopperX,grassHopperY)
        self.isDead = False
        data.xDist = data.plant.x - self.x
        data.yDist = data.plant.y - self.y  
        self.xSpeed = data.xDist / 150
        self.ySpeed = data.yDist / 150
        self.shapeNum = 5
        self.shapeVals = ["n","v","horizontalLine","verticalBar"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
        self.bugType = data.hopperImg 
        self.reborn = False

class LadyBug(Boss):
    def __init__(self,data):
        self.direction = True 
        self.lives = 2
        #This is the number of times each string of things need to be eliminated 
        ratio = (8/10)
        LadyBugX = data.width
        LadyBugY = data.height * ratio
        #starts at the same location at the right of the screen 
        (self.x,self.y) = (LadyBugX,LadyBugY)
        self.isDead = False
        data.xDist = data.plant.x - self.x
        data.yDist = data.plant.y - self.y  
        mediumRatio = 140
        self.xSpeed = data.xDist / mediumRatio
        self.ySpeed = data.yDist / mediumRatio
        self.shapeNum = 6
        self.shapeVals = ["n","v","horizontalLine","verticalBar"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
        self.bugType = data.ladyBugImg 
        self.reborn = False

class Beetle(Boss):
    def __init__(self,data):
        self.direction = True 
        self.lives = 2
        #This is the number of times each string of things need to be eliminated 
        ratio = (8/10)
        LadyBugX = data.width
        LadyBugY = data.height * ratio
        #starts at the same location at the right of the screen 
        (self.x,self.y) = (LadyBugX,LadyBugY)
        self.isDead = False
        data.xDist = data.plant.x - self.x
        data.yDist = data.plant.y - self.y  
        mediumRatio = 140
        self.xSpeed = data.xDist / mediumRatio
        self.ySpeed = data.yDist / mediumRatio
        self.shapeNum = 6
        self.shapeVals = ["n","v","horizontalLine","verticalBar"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
        self.bugType = data.beetleBugImg 
        self.reborn = False


def buildShapes(num, vals):
    #builds up the shapes that each bug contains 
    result = []
    for i in range(num):
        new = random.choice(vals)
        result.append(new)
    return result 


def getBorders(width,height,data):
    step = 10
    #returns a list of locations that are on the outer frame of the canvas 
    border = []
    xVals = [0, width]
    yVals = [data.upperMargin, height]
    for x in xVals:
        for y in range(data.upperMargin,height,step):
        #This is so that no bugs overlap with the hearts and score 
            border.append((x,y))
    for y in yVals:
       for x in range(0,width,step):
           border.append((x,y))
    return border

####################################
# Main(playMode)
####################################

def init(data):
    preloadImages(data)
    data.gameOver = False
    data.upperMargin = 170
    #leaves room for lives and score
    data.plant = Plant(data)
    data.doodle = []
    data.scoreUnit = 1
    initLevel(data)
    data.playMode = "readySetGoMode"
    data.score = 0

def preloadImages(data):
    #This laods in all the images as PIL format
    data.PILplantImg = Image.open("seed.gif")
    data.fleaImg = Image.open("flea.gif")
    data.pillarImg = Image.open("pillar.gif")
    data.splatImg = Image.open("splat.gif")
    data.hopperImg = Image.open("hopper.gif")
    data.ladyBugImg = Image.open("ladybug.gif")
    data.beetleBugImg = Image.open("beetle.gif")


def initLevel(data):
    data.bossCreated = False
    data.LevelTimer = 0
    data.bossDead = False
    data.timer = 0
    data.bugTimer = 0
    data.bugs = []
    data.bugCount = 1
    data.bugs.append(Bug(data))
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

def timerFired(data):
    if data.playMode == "mainPlayMode":
        mainPlayModeTimerFired(data)
    elif data.playMode == "readySetGoMode":
        readySetGoModeTimerFired(data)

def readySetGoModeTimerFired(data):
    millisecond = 1000
    data.LevelTimer += (data.timerDelay/millisecond) 
    if data.LevelTimer > 7:
        data.playMode = "mainPlayMode"

def mainPlayModeTimerFired(data):
    millisecond = 1000
    data.timer += (data.timerDelay/millisecond) 
    data.bugTimer += (data.timerDelay/millisecond) 
    #bug timer is used to create "waves" of bugs 
    generateBugs(data)

    if data.bugs != []:
        for bug in data.bugs:
            if bug.isDead == False:
                bug.move(data)
                bug.updateDeath(data)
    updateLevel(data)

####################################
# Level Update 
####################################
def updateLevel(data):
    #checks if the level is complete
    if data.plant.level == 1:
        #level 1 ends at 20 bugs 
        #eliminate the boss
        level1UpdateLevel(data)
    elif data.plant.level == 2:
        #level 2 ends at 25 bugs 
        #eliminate the boss
        level2UpdateLevel(data)
    elif data.plant.level == 3:
        #level 2 ends at 30 bugs
        #eliminate the boss
        level3UpdateLevel(data)
    elif data.plant.level == 4:
        #level 2 ends at 35 bugs 
        #eliminate the boss
        level4UpdateLevel(data)
    elif data.plant.level == 5:
        #level 2 ends at 40 bugs
        #eliminate the boss
        level5UpdateLevel(data)


def level1UpdateLevel(data):
    if data.levelComplete == False and data.bossDead == True:
        data.levelComplete = True

    if data.levelComplete == True:
        data.plant.level += 1 
        initLevel(data)
        #transition Page 
        data.playMode = "readySetGoMode"
        #move to next level 

def level2UpdateLevel(data):
    if data.levelComplete == False and data.bossDead == True:
        data.levelComplete = True

    if data.levelComplete == True:
        data.plant.level += 1 
        initLevel(data)
        #transition Page 
        data.playMode = "readySetGoMode"
        #move to next level 

def level3UpdateLevel(data):
    if data.levelComplete == False and data.bossDead == True:
        data.levelComplete = True

    if data.levelComplete == True:
        data.plant.level += 1 
        initLevel(data)
        #transition Page 
        data.playMode = "readySetGoMode"
        #move to next level 
def level4UpdateLevel(data):
    if data.levelComplete == False and data.bossDead == True:
        data.levelComplete = True

    if data.levelComplete == True:
        data.plant.level += 1 
        initLevel(data) 
        #transition Page 
        data.playMode = "readySetGoMode"
        #move to next level 

def level5UpdateLevel(data):
    if data.levelComplete == False and data.bossDead == True:
        data.levelComplete = True

    if data.levelComplete == True:
        data.playMode = "GameCompleteMode"
        #move to next level 

####################################
# Bug Generation 
####################################
def generateBugs(data):
    #This generates the bugs that are in the game and append to data.bugs 
    if data.plant.level == 1:
        #level 1 is easy and bugs appear less frequently
        level1GenerateBugs(data)
    elif data.plant.level == 2:
        #level 2 is more difficult and bugs appear more frequently 
        level2GenerateBugs(data)
    elif data.plant.level == 3:
        #level 3 is difficult and bugs appear in swarms 
        level3GenerateBugs(data)
    elif data.plant.level == 4:
        #level 4 is hard and there are a lot of bugs in swarms 
        level4GenerateBugs(data)
    elif data.plant.level == 5:
        #level 5 is very hard and you must use special operators to win
        level5GenerateBugs(data)

def level1GenerateBugs(data):
    #bugs come one at a time every 5 seconds
    if data.bugTimer > 5 and data.bugCount < 5:
        if random.randint(0,1) > 0.5:
            num =random.choice([1,2,3])
            # this generates a wave of bugs that could be between 1 and 3
            for i in range(num):
                data.bugs.append(Bug(data))
                data.bugCount += 1
        else:
            data.bugs.append(Bug(data))
            data.bugCount += 1
        data.bugTimer = 0
        print(data.bugCount)
    elif data.bugTimer > 5 and data.bugCount >= 5 and data.bossCreated == False:
        print("a boss gets generated")
    #the boss only gets generated after the first 20 bugs are created 
    #by doing this we set restrictions on how many bugs must be endured to 
    #complete the level
        # if len(data.bugs) > 0  and not isinstance(data.bugs[-1],GrassHopper):
        # #This makes sure there is one boss that gets generated
        data.bugs.append(GrassHopper(data))
        data.bossCreated = True
        #this is the level 1 boss

def level2GenerateBugs(data):
    #small "waves" of bugs
    #fight boss while fending off small fast bugs 
    if data.bugTimer > 6 and data.bugCount < 18:
        if random.randint(0,1) > 0.5:
            num =random.choice([2,3,4])
            # this generates a wave of bugs that could be between 2 and 4
            for i in range(num):
                data.bugs.append(Bug(data))
                data.bugCount += 1
        else:
            data.bugs.append(Bug(data))
            data.bugCount += 1
        data.bugTimer = 0

    elif data.bugTimer > 4 and data.bugCount >= 18:
        data.bugs.append(Bug(data))
        data.bugs.append(Bug(data))
        data.bugCount += 2
        data.bugTimer = 0

    if data.bugCount >= 18 and data.bossCreated == False:
        #This makes sure there is one boss that gets generated
        data.bugs.append(LadyBug(data))
        #this is the level 2 boss
        data.bossCreated = True

def level3GenerateBugs(data):
    #bigger "waves" of bugs
    if data.bugTimer > 4 and data.bugCount < 30:
        if random.randint(0,1) > 0.6:
            num =random.choice([3,4,5])
            # this generates a wave of bugs that could be between 3 and 5
            for i in range(num):
                data.bugs.append(Bug(data))
                data.bugCount += 1
        else:
            data.bugs.append(Bug(data))
            data.bugCount += 1
        data.bugTimer = 0
    if data.bugTimer > 5 and data.bugCount > 30:
        if len(data.bugs) > 0  and not isinstance(data.bugs[-1],GrassHopper):
        #This makes sure there is one boss that gets generated
            data.bugs.append(GrassHopper(data))
            #this is the level 3 boss

def level4GenerateBugs(data):
    if data.bugTimer > 4 and data.bugCount < 35:
        if random.randint(0,1) > 0.6:
            num =random.choice([3,4,5])
            # this generates a wave of bugs that could be between 3 and 5
            for i in range(num):
                data.bugs.append(Bug(data))
                data.bugCount += 1
        else:
            data.bugs.append(Bug(data))
            data.bugCount += 1
        data.bugTimer = 0
    elif data.bugTimer > 5 and data.bugCount > 35:
        if len(data.bugs) > 0  and not isinstance(data.bugs[-1],GrassHopper):
        #This makes sure there is one boss that gets generated
            data.bugs.append(GrassHopper(data))
            #this is the level 4 boss

def level5GenerateBugs(data):
    if data.bugTimer > 4 and data.bugCount < 40:
        if random.randint(0,1) > 0.6:
            num =random.choice([3,4,5,6])
            # this generates a wave of bugs that could be between 3 and 6
            for i in range(num):
                data.bugs.append(Bug(data))
                data.bugCount += 1
        else:
            data.bugs.append(Bug(data))
            data.bugCount += 1
        data.bugTimer = 0

    elif data.bugTimer > 5 and data.bugCount > 40:
        if len(data.bugs) > 0 and not isinstance(data.bugs[-1],GrassHopper):
        #This makes sure there is one boss that gets generated
            data.bugs.append(GrassHopper(data))
            #this is the level 5 boss

####################################
# RedrawAll
####################################
def redrawAll(canvas, data):
    #background
    color = rgbString(213,219,247 )
    canvas.create_rectangle(-10,-10,data.width+10,data.height+10,fill = color,width = 0)
    if data.playMode == "mainPlayMode":
        mainPlayModeDraw(canvas,data) 

    elif data.playMode == "readySetGoMode":
        readySetGoModeDraw(canvas,data) 

    elif data.playMode == "gameCompleteMode":
        gameCompleteDraw(canvas,data) 

    elif data.playMode == "gameOverMode":
        gameOverModeDraw(canvas,data)        

def mainPlayModeDraw(canvas,data):
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

def readySetGoModeDraw(canvas,data):
    congratsDisplayTime = 3
    drawTime = congratsDisplayTime +3
    setTime = congratsDisplayTime +2
    if data.LevelTimer > drawTime:
        text = "Draw!"
    elif data.LevelTimer > setTime:
        text = "Set"
    elif data.LevelTimer > congratsDisplayTime +1:
        text = "Ready"
    elif data.LevelTimer > congratsDisplayTime:
        text = "Level " + str(data.plant.level) 
    else: 
        if data.plant.level == 1:
            text = "Draw what you see"  
        else:
            text = "Congrats!"
    Arcade90 = font.Font(family='ArcadeClassic',
        size=90, weight='bold')
    canvas.create_text(data.width/2,data.height/2,text = text,font = Arcade90)

def gameCompleteDraw(canvas,data):
    pass

def gameOverModeDraw(canvas,data):
    pass

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
    canvas.create_text(data.width - 100, margin,text = text,anchor = NE, 
        font = Arcade90)

def drawLives(canvas,data):
    #draws the remaining lives at top left
    margin = 60
    total = 5
    lives = data.plant.lives 
    lost = total - lives
    text = "* " * lives + "| " * lost 
    # in this special font "*" is a full heart 
    # "|" is an empty heart that represents life lost
    Heart40 = font.Font(family='My Big Heart Demo',
        size=40, weight='bold')
    canvas.create_text(margin, margin,text = text,anchor = NW, font = Heart40)

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
