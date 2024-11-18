from cmu_graphics import *

def onAppStart(app):
    app.page = "mainpage"
    app.width = 1000
    app.height = 1000
    app.musicList = {
        "homepage": Sound("https://vgmsite.com/soundtracks/new-super-luigi-u-2019/ztszdhxgsu/01.%20Title%20Theme.mp3")
    }
    app.currentMusic = None
    app.musicToggle = True

def onKeyPress(app, key):
    if key == 'm':
        app.musicToggle = not app.musicToggle
        updateMusic(app)

def updateMusic(app):
    if app.musicToggle:
        if app.currentMusic is None:
            app.currentMusic = app.musicList[app.page]
            if app.currentMusic:
                app.currentMusic.play(loop=True)
    else:
        if app.currentMusic:
            app.currentMusic.pause()

def changePage(app, newPage):
    app.page = newPage
    if app.currentMusic:
        app.currentMusic.stop()
    app.currentMusic = app.musicList[app.page]
    updateMusic(app)

def redrawAll(app):
    if app.page == "homepage":
        drawLabel("Beggar Life", 500, 100, size=64)
        drawLabel("Unlock your true money grabbing potential", 500, 175, size=32)
        
        musicStatus = "Music: ON" if app.musicToggle else "Music: OFF"
        drawLabel(musicStatus, 900, 50, size=20)
    
    if app.page == "mainpage":
        drawLabel("This is Mainpage", 500, 100, size = 64)
        drawRect(220,725,260,775, fill = None , borderWidth = 5, border = "black")
        drawLabel("Start Game", 300, 750, size = 16)
        drawLabel("Credits", 600, 750, size = 16)
        drawLabel("Credits#2", 900, 750, size = 16)
        

def main():
    runApp()


main()
