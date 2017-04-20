#################################################
# Init
#################################################
def init(data):
    mainScreenModeInit(data)
    helperScreenModeInit(data)
    playModeInit(data)
    gameOverModeInit(data)
    data.mode = "mainScreenMode"
    data.won = False
    data.paused = False
    

def mainScreenModeInit(data):
    #main screen button 
    data.mplayButtonPressed = False
    data.mhelpButtonPressed = False

def helperScreenModeInit(data):
    #initializes everything in helperScreen mode
    data.hbackButtonPressed = False


def playModeInit(data):
    data.paused = False

def gameOverModeInit(data):
    #initializes everything used in gameOver mode
    pass

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
    elif data.mode == "gameOverMode":
        gameOverModeMousePressed(event,data)
        
        

def mainScreenModeMousePressed(event,data):
    pass

def helperModeMousePressed(event,data):
    pass

def playModeMousePressed(event,data):
    pass

def gameOverModeMousePressed(event,data):
    pass

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
    elif data.mode == "gameOverMode":
        gameOverModeKeyPressed(event,data)

def mainScreenModeKeyPressed(event,data):
    pass

def helperScreenModeKeyPressed(event,data):
    pass

def playModeKeyPressed(event,data):
    pass

def gameOverModeKeyPressed(event,data):
    pass

#################################################
# TimerFired
#################################################

def timerFired(data):
    if data.mode == "mainScreenMode":
        mainScreenModeTimerFired(data)
    elif data.mode == "helperScreenMode":
        helperScreenModeTimerFired(data)
    elif data.mode == "playMode":
        playModeTimerFired(data)
    elif data.mode == "gameOverMode":
        gameOverModeTimerFired(data)

def mainScreenModeTimerFired(data):
    pass

def helperScreenModeTimerFired(data):
    pass

def playModeTimerFired(data):
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
    elif data.mode == "gameOverMode":
        gameOverModeDraw(canvas,data)
        
def mainScreenModeDraw(canvas,data):
    pass

def helperScreenModeDraw(canvas,data):
    pass

def playModeDraw(canvas,data):
    pass

def gameOverModeDraw(canvas,data):
    pass

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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#################################################
# main
#################################################
def runGameLikeApp():
    run(300, 300)

runGameLikeApp()
