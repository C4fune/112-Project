from cmu_graphics import *
import math
def onAppStart(app):
    app.page = "mainpage"
    app.width = 1000
    app.height = 1000
    
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
    app.fov = math.pi 
    app.rayCount = 200
    app.movespeed = 0.1
    app.rotateSpeed = 0.1

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
    
def onKeyHold(app, keys):
    if 'w' in keys:
        moveFunction(app, app.movespeed)
    if 's' in keys:
        moveFunction(app, -app.movespeed)
    if 'a' in keys:
        app.playerAngle -= app.rotateSpeed
    if 'd' in keys:
        app.playerAngle += app.rotateSpeed
    
def moveFunction(app, distanceMoved):
    newX = app.playerX + math.cos(app.playerAngle) * distanceMoved
    newY = app.playerY + math.sin(app.playerAngle) * distanceMoved
    
    if(app.worldMap[int(newX)][int(newY)] == 0):
        app.playerX = newX
        app.playerY = newY

        
def redrawAll(app):

    drawRect(0, 0, app.width, app.height/2, fill='white')
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
        color = rgb(255 - min(255, int(distance * 40)), 0, 0)
        drawLine(x, app.height/2 - wallHeight/2, x, app.height/2 + wallHeight/2, fill=color, lineWidth = 5)
    

def main():
    runApp()
main()


"""
Draw Function Currently (12/2/24)
dx = self.x - app.playerX
dy = self.y - app.playerY

# Calculate angle and distance
angle = math.atan2(dy, dx)
distance = math.sqrt(dx**2 + dy**2)

# Check if page is in player's field of view
relative_angle = angle - app.playerAngle
if abs(relative_angle) < app.fov/2:
    if self.has_line_of_sight(app):
        # Calculate page's screen position
        page_screen_x = app.width/2 + math.tan(relative_angle) * app.width/2
        page_height = min(app.height, app.height / (distance + 0.0001)) 
        page_width = page_height / 2  # Maintain aspect ratio
        
        # Draw page image
        drawImage(self.image_url, page_screen_x - page_width/2, app.height/2 - page_height/2, width=page_width, height=page_height)
"""