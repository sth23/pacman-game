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
    mouth_closed = CircleAsset(20, yellow)
    #mouth_open
    
    def __init__(self, width, height):
        super().__init__(mouth_closed, (width / 2, height * 2 / 3))
        self.vx = 0
        self.vy = 0
        self.fxcenter = self.fycenter = 0
        
    def step(self):
        self.x += self.vy
        self.y += self.vy
        