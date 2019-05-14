"""
Final Project: Pacman
Author: Sean
Credit: Tutorials
Assignment: Create an old-school Pacman game
"""

from ggame import App, RectangleAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

class Wall(Sprite):
    def __init__(self, asset, position):
        super().__init__(asset, position)

class Pacman(Sprite):
    yellow = Color(0xffff00, 1.0)
    noline = LineStyle(0, yellow)
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
        
    def step(self):
        self.x += self.vx
        self.y += self.vy
        
class PacmanGame(App):
    def __init__(self):
        super().__init__()
        self.player1 = Pacman((self.width / 2, self.height * 2 / 3))
        
        # Create game board
        self.black = Color(0, 1)
        self.noline = LineStyle(0, self.black)
        topwall = Wall((0,0, RectangleAsset(self.width, 10, self.noline, self.black))
        
    def step(self):
        self.player1.step()
        
myapp = PacmanGame()
myapp.run()