import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
import random

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt, vecToFollow = None):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        if (vecToFollow):
            direction = self.getDirectionFromVector(vecToFollow)
        else:
            direction = self.getRandomDirection()
        # direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def getDirectionFromVector(self, vector):
        if abs(vector.x) > abs(vector.y):
            # Move horizontally
            if (vector.x > 0):
                dir = RIGHT
            else:
                dir = LEFT
        else:
            # Move vertically
            if (vector.y > 0):
                dir = DOWN
            else:
                dir = UP
        
        # Prevents pacman be stucked on
        if not self.validDirection(dir):
            if abs(vector.x) > abs(vector.y):
                if abs(vector.y > 0):
                    dir = self.getDirectionFromVector(Vector2(0, vector.y))
                elif (self.validDirection(DOWN)):
                    dir = DOWN
                else:
                    dir = UP
            else:
                if abs(vector.x > 0):
                    dir = self.getDirectionFromVector(Vector2(vector.x, 0))
                elif (self.validDirection(RIGHT)):
                    dir = RIGHT
                else:
                    dir = LEFT

        return dir
            
    def getRandomDirection(self):
        vectorX = random.randint(-9,9)
        vectorY = random.randint(-9,9)
        vector = Vector2(vectorX, vectorY)
        direction = self.getDirectionFromVector(vector)
        return direction

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
