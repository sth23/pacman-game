"""
Final Project: Pacman
Author: Sean
Credit: Tutorials
Assignment: Create an old-school Pacman game
"""

from ggame import App, RectangleAsset, CircleAsset, PolygonAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

# Colors & lines
red = Color(0xff0000, 1.0)
orange = Color(0xffa500, 1.0)
yellow = Color(0xffff00, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
purple = Color(0x800080, 1.0)
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
gray = Color(0x888888, 0.5)
noline = LineStyle(0, black)
whiteline = LineStyle(1, white)

class Wall(Sprite):
    def __init__(self, asset, position):
        super().__init__(asset, position)
        
class Dot(Sprite):
    circ = CircleAsset(5, noline, white)
    
    def __init__(self, position):
        super().__init__(Dot.circ, position, CircleAsset(5))
        
class BigDot(Sprite):
    circ = CircleAsset(8, noline, white)
    
    def __init__(self, position):
        super().__init__(BigDot.circ, position)
        
class Ghost(Sprite):
    def __init__(self, position, color, radius):
        self.circ = CircleAsset(radius, noline, color)
        super().__init__(self.circ, position, CircleAsset(radius))
        self.vx = 0
        self.vy = 0
        self.speed = 3
        self.count = 0
        self.chance = 0
        
    def goRight(self):
        self.vx = self.speed
        self.vy = 0
        
    def goLeft(self):
        self.vx = -self.speed
        self.vy = 0
    
    def goUp(self):
        self.vy = -self.speed
        self.vx = 0
        
    def goDown(self):
        self.vy = self.speed
        self.vx = 0
        
    def hitWall(self):
        self.x -= self.vx
        self.y -= self.vy
        self.count += 10
        
        if self.vy != 0:
            self.vy = 0
            self.chance = random.randint(0,2)
            if self.chance == 0:
                self.vx = self.speed
            else:
                self.vx = -self.speed
        else:
            self.vx = 0
            self.chance = random.randint(0,2)
            if self.chance == 0:
                self.vy = self.speed
            else:
                self.vy = -self.speed
                
    def hitGhost(self):
        self.x -= self.vx
        self.y -= self.vy
        self.vx = -self.vx
        self.vy = -self.vy
        self.count += 10
        
    def step(self):
        if self.count % 50 == 0:
            self.chance = random.randint(0,3)
            if self.chance == 0:
                self.goRight()
            elif self.chance == 1:
                self.goLeft()
            elif self.chance == 2:
                self.goUp()
            else:
                self.goDown()
        self.count += 1
                
        self.x += self.vx
        self.y += self.vy

class PacMouth(Sprite):
    def __init__(self, x, y, vx, vy, radius):
        self.vx = vx
        self.vy = vy
        self.radius = radius + 1
        self.count = 0
        self.poly = [None] * int(self.radius * 3 / 4)
        for x in range(0,int(self.radius * 3 / 4)):
            self.poly[x] = PolygonAsset([(0,0), (self.radius, self.radius * 3 / 4 - x), (self.radius, -self.radius * 3 / 4 - x)], noline, black)
        super().__init__(self.poly[0], (x, y))
        self.rotation = 0
        self.fycenter = 0.5
        
    def step(self):
        if self.vx > 0:
            self.rotation = 0
        elif self.vx < 0:
            self.rotation = math.pi
        elif self.vy > 0:
            self.rotation = math.pi * 3 / 2
        elif self.vy < 0:
            self.rotation = math.pi / 2
            
class Pacman(Sprite):
    def __init__(self, position, radius):
        self.radius = radius
        self.circ = CircleAsset(self.radius, noline, yellow)
        super().__init__(self.circ, position, CircleAsset(self.radius))
        self.vx = 0
        self.vy = 0
        self.speed = 3
        self.fxcenter = self.fycenter = 0.5
        self.gameover = False
        
        self.mouth = PacMouth(self.x, self.y, self.vx, self.vy, self.radius)
        
        # Setup Player Controls
        PacmanGame.listenKeyEvent("keydown", "right arrow", self.goRight)
        PacmanGame.listenKeyEvent("keydown", "left arrow", self.goLeft)
        PacmanGame.listenKeyEvent("keydown", "up arrow", self.goUp)
        PacmanGame.listenKeyEvent("keydown", "down arrow", self.goDown)
        
    def goRight(self, event):
        self.vx = self.speed
        self.vy = 0
        
    def goLeft(self, event):
        self.vx = -self.speed
        self.vy = 0
    
    def goUp(self, event):
        self.vy = -self.speed
        self.vx = 0
        
    def goDown(self, event):
        self.vy = self.speed
        self.vx = 0
        
    def hitWall(self):
        self.x -= self.vx
        self.y -= self.vy
        self.vx = 0
        self.vy = 0
        
    def step(self):
        if self.gameover == False:
            self.x += self.vx
            self.y += self.vy
            self.mouth.x = self.x
            self.mouth.y = self.y
            self.mouth.vx = self.vx
            self.mouth.vy = self.vy
            self.mouth.step()
        
class PacmanGame(App):
    def __init__(self):
        super().__init__()
        bg_asset = RectangleAsset(self.width, self.height, noline, black)
        bg = Sprite(bg_asset, (0,0))
        
        # Variable to handle pausing / unpausing
        self.paused = True
        PacmanGame.listenKeyEvent("keydown", "space", self.pause)
        
        # Create grid of walls & dots
        self.wallwidth = 10
        self.numcolumns = 10
        self.blockwidth = int(self.width / 40)
        self.lanewidth = (self.width - self.wallwidth * 2 - self.blockwidth * self.numcolumns) / (self.numcolumns + 1)
        self.numrows = round((self.height - self.wallwidth * 2 - self.lanewidth) / (self.blockwidth + self.lanewidth))
        self.laneheight = (self.height - self.wallwidth * 2 - self.blockwidth * self.numrows) / (self.numrows + 1)
        self.blocks = RectangleAsset(self.blockwidth, self.blockwidth, whiteline, blue)
        
        self.pacradius = ((self.lanewidth + self.laneheight) / 2) / 4
        
        # Create player
        self.player1 = Pacman((self.width / 2 - 30, 35), self.pacradius)
        self.score = 0
        self.extralives = 3
        
        # Create ghosts
        self.blueghost = Ghost((self.width / 6, self.height - 60), blue, self.pacradius)
        self.purpleghost = Ghost((self.width * 2 / 6, self.height - 60), purple, self.pacradius)
        self.redghost = Ghost((self.width * 3 / 6, self.height - 60), red, self.pacradius)
        self.orangeghost = Ghost((self.width * 4 / 6, self.height - 60), orange, self.pacradius)
        self.greenghost = Ghost((self.width * 5 / 6, self.height - 60), green, self.pacradius)
        self.ghostcount = 1
        
        self.makeWalls()
        self.makeBlocks()
        self.makeDots()
        self.dotcount = (self.numrows + 1) * (self.numcolumns + 1)
        
    
    def makeWalls(self):        
        # Create game board
        topwall = Wall(RectangleAsset(self.width, self.wallwidth, whiteline, blue), (0, 0))
        rightwall = Wall(RectangleAsset(self.wallwidth, self.height, whiteline, blue), (self.width - self.wallwidth, 0))
        leftwall = Wall(RectangleAsset(self.wallwidth, self.height, whiteline, blue), (0, 0))
        bottomwall = Wall(RectangleAsset(self.width, self.wallwidth, whiteline, blue), (0, self.height - self.wallwidth))
        
    def makeBlocks(self):
        # Create block grid
        for x in range(0, self.numcolumns + 1):
            for y in range(0, self.numrows + 1):
                #Wall(self.blocks, (10 + self.lanewidth * (x + 1) + self.blockwidth * x, 20))
                Wall(self.blocks, (x * self.lanewidth + (x - 1) * self.blockwidth, y * self.laneheight + (y - 1) * self.blockwidth))
        
    def makeDots(self):
        # Create dots
        self.dotcount = 66
        for x in range(0, self.numcolumns + 2):
            for y in range(0, self.numrows + 2):
                Dot(((x - 0.5) * self.lanewidth + (x - 1) * self.blockwidth, (y - 0.5) * self.laneheight + (y - 1) * self.blockwidth))
                
    def resetGhosts(self):
        for ghost in self.getSpritesbyClass(Ghost):
            ghost.x = self.width * self.ghostcount / 6
            ghost.y = self.height - 60
            self.ghostcount += 1
        self.ghostcount = 1
        
    def pause(self, event):
        self.paused = not self.paused
        
    def step(self):
        if self.paused == False:
            self.player1.step()
            
            # Handle ghosts colliding w/ walls and other ghosts
            for ghost in self.getSpritesbyClass(Ghost):
                if ghost.collidingWithSprites(Ghost):
                    ghost.hitGhost()
                if ghost.collidingWithSprites(Wall):
                    ghost.hitWall()
                ghost.step()
            
            # Handle player colliding with walls    
            if self.player1.collidingWithSprites(Wall):
                self.player1.hitWall()
                
            # Handle player eating dots
            for dot in self.player1.collidingWithSprites(Dot):
                dot.destroy()
                self.dotcount -= 1
                self.score += 10
                print("Score: " + str(self.score))
                
            # Handle player colliding with ghosts
            if self.player1.collidingWithSprites(Ghost):
                if self.player1.gameover == False:
                    self.player1.x = self.width / 2 - 30
                    self.player1.y = 35
                    self.player1.vx = 0
                    self.player1.vy = 0
                    self.resetGhosts()
                    if self.extralives == 0:
                        self.player1.gameover = True
                        print("Game Over")
                    else:
                        self.extralives -= 1
                        self.paused = not self.paused
                        print("Extra Lives: " + str(self.extralives))
                
            # Reset board @ end of level
            if self.dotcount == 0:
                self.player1.x = self.width / 2 - 30
                self.player1.y = 35
                self.player1.vx = 0
                self.player1.vy = 0
                self.makeDots()
                self.resetGhosts()
                for ghost in self.getSpritesbyClass(Ghost):
                    ghost.speed = ghost.speed + 0.5
                self.paused = not self.paused
        
myapp = PacmanGame()
myapp.run()
