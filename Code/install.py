from cmu_graphics import *

def onAppStart(app):
    app.level = 0
    app.width = 1000
    app.height = 1000

def onKeyPress(app, key):
    pass

def redrawAll(app):
    drawLabel("Beggar Life", 500,100, size = 64)
    drawLabel("Unlock your true money grabbing potential", 500, 175, size = 32)


def main():
    runApp()

main()

