"""
Final Project: Pacman
Author: Sean
Credit: Tutorials
Assignment: Create an old-school Pacman game
"""

from ggame import App, RectangleAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

class Pacman(Sprite):
    yellow = Color(0xffff00, 1.0)
    noline = LineStyle(0, yellow)
    mouth_closed = CircleAsset(20, noline, yellow)
    #mouth_open
    
    def __init__(self, position):
        super().__init__(mouth_closed, position)
        self.vx = 0
        self.vy = 0
        self.fxcenter = self.fycenter = 0
        
    def step(self):
        self.x += self.vy
        self.y += self.vy
        
class PacmanGame(App):
    def __init__(self):
        super().__init__()
        player1 = Pacman((self.width / 2, self.height * 2 / 3))
        
    def step(self):
        player1.step()
        
myapp = PacmanGame()
myapp.run()