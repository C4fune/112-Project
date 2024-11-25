from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.page = "howtopage"
    app.width = 1000
    app.height = 1000
    
    app.music = {
        "homepage": Sound("https://vgmsite.com/soundtracks/new-super-luigi-u-2019/ztszdhxgsu/01.%20Title%20Theme.mp3"),
        "mainpage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3"),
        "introductionpage": Sound("https://kappa.vgmsite.com/soundtracks/mario-kart-ds/pnscoryzve/39.%20Rainbow%20Road.mp3"),
        "creditspage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3"),
        "howtopage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3")
    }

    app.url = {
        "Page1" : 'Code/images/IntroPic.jpg',
        "Monster" : 'Code/images/Kozbie.jpg'
    }

    app.musicOn = True
    app.music[app.page].play(loop=True)
    app.pageObtained = 0

    # init code. 
    app.chunkSize = 8  
    app.currentChunk = (0, 0)  
    app.chunks = {}  
    app.chunks[(0, 0)] = generateInitialChunk()  
    
    #player init position/angle
    app.playerX = 1.5
    app.playerY = 1.5
    app.playerAngle = 0
    app.fov = math.pi / 3
    app.rayCount = 250
    app.moveSpeed = 0.1
    app.rotateSpeed = 0.1

    #border radius settings

    app.borderCircleRadius = 20
    app.circlesPerSide = (app.width // (app.borderCircleRadius * 2)) + 2

    # Monster initialization
    app.monsterX = 6.5  # Start monster away from player
    app.monsterY = 6.5
    app.monsterSpeed = 0.03  # Adjust this to change difficulty
    app.gameOver = False
    app.gameOverOpacity = 0
    
    # Add step counter for monster updates
    app.stepsPerSecond = 30


def generateInitialChunk():
    return [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,1,0,0,1,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,1,0,0,1,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
    ]

def generateNewChunk():
    # Generate a new chunk without border walls
    chunk = [[0 for _ in range(8)] for _ in range(7)]
    
    # Create random walls throughout the chunk
    for y in range(7):
        for x in range(8):
            # THIS 0.3 IS THE CHANCE THERE IS A WALL GENERATED
            # MAKE POSSIBLE CHANGES HERE FOR MORE COMPLEXITY BY CREATING A HIGHER CHANCE OF WALL WITH LEVEL DIFFICULTY
            if random.random() < 0.3 and (x, y) != (1, 1):  # Avoids possiblity wall is generated in the player spawn
                
                chunk[y][x] = 1
    
    # Ensure the chunk has open space (there is a 0 that a user can get into)
    for y in range(7):
        hasPath = False
        for x in range(8):
            if chunk[y][x] == 0:
                hasPath = True
                break
        if not hasPath:
            # Create at least one path if none exists
            x = random.randint(0, 7)
            chunk[y][x] = 0
    
    return chunk

def getChunkCoordinates(app, x, y):
    chunkX = int(x // app.chunkSize)
    chunkY = int(y // app.chunkSize)
    return (chunkX, chunkY)

def getLocalCoordinates(app, x, y):

    # Ensure coordinates wrap within chunk boundaries
    localX = int(x % app.chunkSize)
    localY = int(y % app.chunkSize)

    # Prevent accessing out of bounds indices
    localX = min(localX, 7)  # 8 wide (0-7)
    localY = min(localY, 6)  # 7 tall (0-6)
    
    return (localX, localY)

def checkAndGenerateChunks(app, x, y):
    currentChunk = getChunkCoordinates(app, x, y)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighborChunk = (currentChunk[0] + dx, currentChunk[1] + dy)
            if neighborChunk not in app.chunks:
                app.chunks[neighborChunk] = generateNewChunk()

def getWallAt(app, x, y):
    chunkCoords = getChunkCoordinates(app, x, y)
    if chunkCoords not in app.chunks:
        return 1  # Return wall if chunk doesn't exist
    
    try:
        localX, localY = getLocalCoordinates(app, x, y)
        return app.chunks[chunkCoords][localY][localX]
    except IndexError:
        # If we somehow still get an index error, return a wall
        return 1

def onKeyPress(app, key):
    if key == 'm':
        toggleMusic(app)
    elif key == 'r' and app.gameOver:
        # Reset game
        app.playerX = 1.5
        app.playerY = 1.5
        app.monsterX = 6.5
        app.monsterY = 6.5
        app.gameOver = False
        app.chunks = {}
        app.chunks[(0, 0)] = generateInitialChunk()

def onKeyHold(app, keys):
    if app.page == "mainpage":
        if ('a' in keys or 'left' in keys):
            app.playerAngle -= app.rotateSpeed
        if ('d' in keys or 'right' in keys):
            app.playerAngle += app.rotateSpeed
        if ('w' in keys or 'up' in keys):
            movePlayer(app, app.moveSpeed)
        if ('s' in keys or 'down' in keys):
            movePlayer(app, -app.moveSpeed)

def onMousePress(app, mouseX, mouseY):
    if app.page == "homepage":
        if 180 <= mouseX <= 320 and 725 <= mouseY <= 775:
            app.music[app.page].pause()
            app.page = "mainpage"
            if app.musicOn:
                app.music[app.page].play(loop=True)
        if 430 <= mouseX <= 570 and 725 <= mouseY <= 775:
            app.music[app.page].pause()
            app.page = "howtopage"
            if app.musicOn:
                app.music[app.page].play(loop=True)
        if 680 <= mouseX <= 820 and 725 <= mouseY <= 775:
            app.music[app.page].pause()
            app.page = "creditspage"
            if app.musicOn:
                app.music[app.page].play(loop=True)
    
    if (app.page != "homepage" and app.page != "mainpage"):
        if 825 <= mouseX <= 975 and 85 <= mouseY <= 135:
            app.music[app.page].pause()
            app.page = "homepage"
            if app.musicOn:
                app.music[app.page].play(loop=True)

def toggleMusic(app):
    if app.musicOn:
        app.music[app.page].pause()
        app.musicOn = False
    else:
        app.music[app.page].play(loop=True)
        app.musicOn = True

def movePlayer(app, distance):
    newX = app.playerX + math.cos(app.playerAngle) * distance
    newY = app.playerY + math.sin(app.playerAngle) * distance
    
    # Ensure coordinates stay within valid ranges
    if newX < 0: newX = 0
    if newY < 0: newY = 0
    
    checkAndGenerateChunks(app, newX, newY)
    
    # Only move if the new position is not a 1 (wall)
    try:
        if getWallAt(app, newX, newY) == 0:
            app.playerX = newX
            app.playerY = newY
    except IndexError:
        pass  # SKIP

def castRay(app, angle):
    x, y = app.playerX, app.playerY
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    try:
        while True:
            x += 0.1 * cos_a
            y += 0.1 * sin_a
            
            if x < 0 or y < 0:  #(this is kinda bruteforcing to ensure we dont get negative coordinate) SUBJECT TO CHANGE IF I HAVE TIME (IT WORKS FOR NOW)
                return math.sqrt((x - app.playerX)**2 + (y - app.playerY)**2)
            
            # Check if any chunk hits a wall (good for us)
            if getWallAt(app, x, y) == 1:
                distance = math.sqrt((x - app.playerX)**2 + (y - app.playerY)**2)
                return distance
            
    except IndexError: 
        return math.sqrt((x - app.playerX)**2 + (y - app.playerY)**2) #ensure if there is a calcualtion error in ray casting, we move back to the previous ray position

def updateMonster(app):
    if app.gameOver:
        return
        
    # Calculate direction to player
    dx = app.playerX - app.monsterX
    dy = app.playerY - app.monsterY
    
    # Calculate distance to player
    distance = math.sqrt(dx**2 + dy**2)
    
    # Check for game over condition
    if distance < 0.2:
        app.gameOver = True
        return
        
    # Normalize direction
    if distance > 0:
        dx /= distance
        dy /= distance
    
    # Calculate new position
    app.monsterX = app.monsterX + dx * app.monsterSpeed
    app.monsterY = app.monsterY + dy * app.monsterSpeed
    
    # This function makes it where the monster can walk through walls or not
    #if getWallAt(app, newX, newY) == 0:
       #app.monsterX = newX
       #app.monsterY = newY

def onStep(app):
    if app.page == "mainpage" and not app.gameOver:
        updateMonster(app)



def redrawAll(app):
  
    if app.page == "introductionpage":
        drawLabel("No, this is not Mario Kart", 600, 600, size = 32)
        drawImage(app.url["Page1"], 0, 0)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border="black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size=20)
        drawRect(825, 85, 150, 50, fill=None, border="black", borderWidth=5)
    
    elif app.page == "creditspage":
        drawLabel("This is the creditspage", 200, 200)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border="black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size=20)
        drawRect(825, 85, 150, 50, fill=None, border="black", borderWidth=5)

    elif app.page == "howtopage":
        drawLabel("How to Play 112 BackRooms!", 200, 200)
        drawLabel("There are scary monsters (cough) chasing you in this game..", 200, 300)
        drawLabel("The goal in this game is to run away, while obtaining 8 pages that are randomly distributed throughout the map!", 200, 400)
        drawLabel("Keep in mind that the map is auto generated as you stray away from spawn.", 200, 500)
        drawLabel("You can only see the monster when it is faced in front of you!", 200, 600)
        drawLabel("This means that if you don't see the monster, it might be behind you!", 200, 700)
        drawLabel("There will be a scary sound whenever the monster is close to you!", 200, 800)
        drawImage(app.url["Monster"], 800, 500)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border="black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size=20)
        drawRect(825, 85, 150, 50, fill=None, border="black", borderWidth=5)
        
    elif app.page == "homepage":
        drawLabel("112 BackRooms", 500, 100, size=64)
        drawLabel("Collect 8 pages as you run away from scary monsters!", 500, 175, size=32)
        
        drawRect(180, 725, 140, 50, fill=None, border="black", borderWidth=5)
        drawLabel("Start Game", 250, 750, size=16)
        
        drawRect(430, 725, 140, 50, fill=None, border="black", borderWidth=5)
        drawLabel("How to Play", 500, 750, size=16)

        drawRect(680, 725, 140, 50, fill=None, border="black", borderWidth=5)
        drawLabel("Credits", 750, 750, size=16)
        
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border="black", borderWidth=5)
    
    elif app.page == "mainpage":
        # Draw sky
        drawRect(0, 0, app.width, app.height/2, fill='black')
        # Draw ground
        drawRect(0, app.height/2, app.width, app.height/2, fill='black')
        
        # Cast rays and draw walls
        for i in range(app.rayCount):
            rayAngle = app.playerAngle - app.fov/2 + (i / app.rayCount) * app.fov
            distance = castRay(app, rayAngle)
            
            # Calculate wall height
            wallHeight = min(app.height, app.height / (distance + 0.0001))
            
            # Draw wall slice
            x = i * (app.width / app.rayCount)
            drawLine(x, app.height/2 - wallHeight/2, x, app.height/2 + wallHeight/2, fill="white")
        
        # Draw monster (basic representation)
        monsterAngle = math.atan2(app.monsterY - app.playerY, app.monsterX - app.playerX)
        monsterRelativeAngle = monsterAngle - app.playerAngle
        monsterDistance = math.sqrt((app.monsterX - app.playerX)**2 + (app.monsterY - app.playerY)**2)
        
        # Only draw monster if it's in front of the player
        if abs(monsterRelativeAngle) < app.fov/2:
            # Calculate monster's screen position
            monsterScreenX = app.width/2 + math.tan(monsterRelativeAngle) * app.width/2
            monsterHeight = min(app.height, app.height / (monsterDistance + 0.0001))
            monsterWidth = monsterHeight / 2  # Maintain aspect ratio
            
            # Draw monster using drawImage with the URL directly
            drawImage(app.url["Monster"], monsterScreenX - monsterWidth/2, app.height/2 - monsterHeight/2, width=monsterWidth, height=monsterHeight)
        
        # Draw UI elements
        drawLabel("Use arrow keys to move", 500, 50, size=20, fill='red')
        drawLabel(f"Player Position: ({app.playerX:.2f}, {app.playerY:.2f})", 500, 100, size=20, fill='red')
        drawLabel(f"Distance to Monster: {monsterDistance:.2f}", 500, 150, size=20, fill='red')
        
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20, fill='red')
        drawRect(825, 25, 150, 50, fill=None, border="red", borderWidth=5)

        if app.gameOver:
            drawRect(0, 0, app.width, app.height, 
                     fill='black', opacity=80)
            
            # Draw game over text
            drawLabel("GAME OVER", app.width/2, app.height/2, size=64, fill='red', bold=True)
            drawLabel("Press 'R' to restart", app.width/3, app.height/2 + 100, size=32, fill='red')
            drawLabel("Go Back to Homepage", app.width * 2/3, app.height/2 + 100, size = 32, fill = 'red')

    
    if app.page != 'mainpage': #not mainpage as mainpage is the gameplay page!
        #draw borders, all four sides
        for i in range(app.circlesPerSide):
            x = i * (app.borderCircleRadius * 2)
            drawArc(x, 0, app.borderCircleRadius * 2, app.borderCircleRadius * 2, 180, 180, fill='black')
        for i in range(app.circlesPerSide):
            x = i * (app.borderCircleRadius * 2)
            drawArc(x, app.height, app.borderCircleRadius * 2, app.borderCircleRadius * 2, 0, 180, fill='black')
        for i in range(app.circlesPerSide):
            y = i * (app.borderCircleRadius* 2)
            drawArc(0, y, app.borderCircleRadius * 2, app.borderCircleRadius * 2, 180, 360, fill='black')
        for i in range(app.circlesPerSide):
            y = i * (app.borderCircleRadius * 2)
            drawArc(app.width, y, app.borderCircleRadius * 2, app.borderCircleRadius * 2, 90, 270, fill='black')

def main():
    runApp()

main()