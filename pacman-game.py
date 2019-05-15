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
        self.blueghost = Ghost((0, random.randint(0, self.width)), blue)
        self.purpleghost = Ghost((0, random.randint(0, self.width)), purple)
        self.redghost = Ghost((0, random.randint(0, self.width)), red)
        self.orangeghost = Ghost((0, random.randint(0, self.width)), orange)
        
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
        if self.blueghost.collidingWithSprites(Wall):
            self.blueghost.hitWall()
        if self.purpleghost.collidingWithSprites(Wall):
            self.purpleghost.hitWall()
        if self.yellowghost.collidingWithSprites(Wall):
            self.yellowghost.hitWall()
        if self.orangeghost.collidingWithSprites(Wall):
            self.orangeghost.hitWall()
        if self.player1.collidingWithSprites(Wall):
            self.player1.hitWall()
        for dot in self.player1.collidingWithSprites(Dots):
            dot.destroy()
        
myapp = PacmanGame()
myapp.run()