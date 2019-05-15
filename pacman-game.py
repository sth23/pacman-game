"""
Final Project: Pacman
Author: Sean
Credit: Tutorials
Assignment: Create an old-school Pacman game
"""

from ggame import App, RectangleAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
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
        
class Dots(Sprite):
    circ = CircleAsset(5, noline, white)
    
    def __init__(self, position):
        super().__init__(Dots.circ, position)
        
class BigDots(Sprite):
    circ = CircleAsset(8, noline, white)
    
    def __init__(self, position):
        super().__init__(BigDots.circ, position)
        
class Ghost(Sprite):
    def __init__(self, position, color):
        self.circ = CircleAsset(20, noline, color)
        super().__init__(self.circ, position)
        self.vx = 0
        self.vy = 0
        self.speed = 2.5
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
        self.vx = -self.vx
        self.vy = -self.vy
        
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


class Pacman(Sprite):
    mouth_closed = CircleAsset(20, noline, yellow)
    #mouth_open
    
    def __init__(self, position):
        super().__init__(Pacman.mouth_closed, position)
        self.vx = 0
        self.vy = 0
        self.speed = 2.5
        self.gameover = False
        
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
        
class PacmanGame(App):
    def __init__(self):
        super().__init__()
        bg_asset = RectangleAsset(self.width, self.height, noline, black)
        bg = Sprite(bg_asset, (0,0))
        
        # Create player
        self.player1 = Pacman((self.width / 2, self.height * 2 / 3))
        
        # Create ghosts
        self.blueghost = Ghost((random.randint(20, self.width - 20), random.randint(20, self.height - 20)), blue)
        self.purpleghost = Ghost((random.randint(20, self.width - 20), random.randint(20, self.height - 20)), purple)
        self.redghost = Ghost((random.randint(20, self.width - 20), random.randint(20, self.height - 20)), red)
        self.orangeghost = Ghost((random.randint(20, self.width - 20), random.randint(20, self.height - 20)), orange)
        self.greenghost = Ghost((random.randint(20, self.width - 20), random.randint(20, self.height - 20)), green)
        
        # Create game board
        topwall = Wall(RectangleAsset(self.width, 10, whiteline, blue), (0, 0))
        rightwall = Wall(RectangleAsset(10, self.height, whiteline, blue), (self.width - 10, 0))
        leftwall = Wall(RectangleAsset(10, self.height, whiteline, blue), (0, 0))
        bottomwall = Wall(RectangleAsset(self.width, 10, whiteline, blue), (0, self.height - 10))
        
        # Randomly place dots (to eat)
        for x in range(0,20):
            Dots((random.randint(0, self.width), random.randint(0, self.height)))
        
        # Randomly place walls
        self.blocks = RectangleAsset(30, 30, whiteline, blue)
        for x in range(0,5):
            Wall(self.blocks, (random.randint(0, self.width), random.randint(0, self.height)))
        
    def step(self):
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
        for dot in self.player1.collidingWithSprites(Dots):
            dot.destroy()
            
        # Handle player colliding with ghosts
        if self.player1.collidingWithSprites(Ghost):
            self.player1.gameover = True
            self.player1.vx = 0
            self.player1.vy = 0
        
myapp = PacmanGame()
myapp.run()