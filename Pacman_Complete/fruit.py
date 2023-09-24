import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

class Fruit(Entity):
    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 0 # Set to autodestroy itself at the time of creation
        self.timer = 0
        self.destroy = True # Set to autodestroy itself at the time of creation
        self.points = 100 + level*20
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True