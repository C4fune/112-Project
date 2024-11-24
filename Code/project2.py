from cmu_graphics import *
import math

def onAppStart(app):
    app.page = "introductionpage"
    app.width = 1000
    app.height = 1000
    
    app.music = {"homepage":Sound("https://vgmsite.com/soundtracks/new-super-luigi-u-2019/ztszdhxgsu/01.%20Title%20Theme.mp3"),
                 "mainpage":Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3"),
                 "introductionpage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3"),
                 "creditspage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3"),
                 "howtopage": Sound("https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3")}
    
    app.backgroundPicture = {"introductionpage": 'cmu://872469/35224887/IntroPic.jpg'}

    app.url = 'Code/IntroPic.jpg'
    app.musicOn = True
    app.music[app.page].play(loop=True)

    app.worldMap = [
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,0,0,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,0,0,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
    ]
    app.playerX = 1.5
    app.playerY = 1.5
    app.playerAngle = 0
    app.fov = math.pi / 3
    app.rayCount = 250
    app.moveSpeed = 0.1
    app.rotateSpeed = 0.1

    # Add monster properties - start 1 block away from player
    app.monsterX = 2.5  # Player is at 1.5, so this is 1 block to the right
    app.monsterY = 1.5
    app.monsterSpeed = app.moveSpeed / 2

def updateMonster(app):
    if app.page == "mainpage":
        dx = app.playerX - app.monsterX
        dy = app.playerY - app.monsterY
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            dx = (dx / distance) * app.monsterSpeed
            dy = (dy / distance) * app.monsterSpeed
            
            newX = app.monsterX + dx
            newY = app.monsterY + dy
            if app.worldMap[int(newY)][int(newX)] == 0:
                app.monsterX = newX
                app.monsterY = newY

def onStep(app):
    updateMonster(app)

def onKeyPress(app, key):
    if key == 'm':
        toggleMusic(app)

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
            app.music[app.page].pause()  # Pause current page's music
            app.page = "mainpage"
            if app.musicOn:  # Only play new music if music is on
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
            app.music[app.page].pause()  # Pause current page's music
            app.page = "homepage"
            if app.musicOn:  # Only play new music if music is on
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
    if app.worldMap[int(newY)][int(newX)] == 0:
        app.playerX = newX
        app.playerY = newY

def castRay(app, angle):
    x, y = app.playerX, app.playerY
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    while True:
        x += 0.1 * cos_a
        y += 0.1 * sin_a
        
        map_x, map_y = int(x), int(y)
        
        if app.worldMap[map_y][map_x] == 1:
            distance = math.sqrt((x - app.playerX)**2 + (y - app.playerY)**2)
            return distance

def redrawAll(app):
    if app.page == "introductionpage":
        drawImage(app.url,0,0)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border = "black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size = 20)
        drawRect(825, 85, 150, 50, fill=None, border = "black", borderWidth=5)
    
    if app.page == "creditspage":
        drawLabel("This is the creditspage", 200, 200)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border = "black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size = 20)
        drawRect(825, 85, 150, 50, fill=None, border = "black", borderWidth=5)

    if app.page == "howtopage":
        drawLabel("How to Play 112 BackRooms!", 200, 200)
        drawLabel("There are scary monsters chasing you in this game..", 200, 300)
        drawLabel("The goal in this game is to run away, while obtaining 8 pages that are randomly distributed throughout the map!",200, 400)
        drawLabel("Keep in mind that the map is auto generated as you stray away from spawn.", 200, 500)
        drawLabel("A scary sound will be played whenever the monster is close by.", 200, 600)
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
        drawRect(825, 25, 150, 50, fill=None, border = "black", borderWidth=5)
        drawLabel('To Homepage', 900, 110, size = 20)
        drawRect(825, 85, 150, 50, fill=None, border = "black", borderWidth=5)
        
    if app.page == "homepage":
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
        drawRect(825, 25, 150, 50, fill=None, border = "black", borderWidth=5)
    
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
            color = rgb(255 - min(255, int(distance * 20)), 0, 0)
            drawLine(x, app.height/2 - wallHeight/2, x, app.height/2 + wallHeight/2, fill="white")

        # Draw monster if it's in view
        monsterScreenX = app.width * (1 + math.atan2(app.monsterY - app.playerY, 
                                                    app.monsterX - app.playerX) / app.fov) / 2
        monsterDistance = math.sqrt((app.monsterX - app.playerX)**2 + 
                                  (app.monsterY - app.playerY)**2)
        monsterSize = min(200, 2000 / monsterDistance)
        
        if 0 <= monsterScreenX <= app.width:
            drawImage(app.url, 
                     monsterScreenX - monsterSize/2,
                     app.height/2 - monsterSize/2,
                     width=monsterSize,
                     height=monsterSize)
        
        drawLabel("Use arrow keys to move", 500, 50, size=20, fill = 'red')
        drawLabel(f"Player Position: ({app.playerX:.2f}, {app.playerY:.2f})", 500, 100, size=20, fill = 'red')
        drawLabel(f"Player Angle: {math.degrees(app.playerAngle):.2f}", 500, 150, size=20, fill = 'red')
        
        musicStatus = "Music: ON" if app.musicOn else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20, fill = 'red')
        drawRect(825, 25, 150, 50, fill=None, border = "red", borderWidth=5)

def main():
    runApp()

main()