# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random 

####################################
# Plant 
####################################
class Plant(object):
    def __init__(self):
        self.r = 30
        self.x = 250
        self.y = 250
        self.level = 1
        self.lives = 5
        self.score = 0 
        self.isDead = False

    def updateDeath(self):
        if self.lives <= 0:
            self.isDead = True
    def reduceLives(self,bugs):
        pass
    def draw(self,canvas):
        canvas.create_oval(self.x - self.r,self.y - self.r,self.x + self.r,
                                                self.y + self.r)
class Bug(object):
    def __init__(self,plant):
        startLocations = getBorders(500,500)
        (self.x,self.y) = random.choice(startLocations) 
        self.r = 10
        self.isDead = False
        xDist = plant.x - self.x
        yDist = plant.y - self.y
        if plant.level == 1:
        #level 1 is easy and most bugs contain only 1 shape
            
            self.xSpeed = xDist / 30
            self.ySpeed = yDist / 30 
            if (random.randint(0,1) < 0.1):
                self.shapeNum = random.randint(1,3)
            else:
                self.shapeNum = 1
        #level 2 is easy and most bugs contain only 1 shape
        #level 3 is easy and most bugs contain only 1 shape
        #level 4 is easy and most bugs contain only 1 shape
        #level 5 is difficult and everybug contains 4-9 shapes 
        self.shapeVals = ["square","circle","triangle","star"]
        self.shapesRemaining = buildShapes(self.shapeNum, self.shapeVals)
    def draw(self,canvas):
        canvas.create_oval(self.x - self.r,self.y - self.r,self.x + self.r,
                                                self.y + self.r, fill = "Red")

    def updateDeath(self):
        if self.shapesRemaining == []:
            self.isDead = True

def buildShapes(num, vals):
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

print(getBorders(500,500))



####################################
# customize these functions
####################################

def init(data):
    data.simin = Plant()
    data.ant = Bug(data.simin)
    print(data.ant.x, data.ant.y)
    print(data.ant.shapesRemaining)

def mousePressed(event, data):
    # use event.x and event.y
    data.prevX = event.x
    data.prevY = event.y

def mouseDragged(canvas,event, data):
	print("mouseDragged")
	canvas.create_line(data.prevX,data.prevY,event.x,event.y,width = 6)
	data.prevX,data.prevY = event.x,event.y


def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    data.simin.draw(canvas)

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
        # redrawAllWrapper(canvas, data)

    def mouseDraggedWrapper(event, canvas, data):
    	mouseDragged(canvas,event, data)
    	# redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        # redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        # redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
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

run(500, 500)