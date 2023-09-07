import sys
sys.path.append("../Pacman_Complete")

from Pacman_Complete.constants import *

class UsefulInformation():
    def __init__(self, game_controller):
        self.gc = game_controller

        self.powerMode = False
        self.powerPelletsAvailable = False

        self.iVecToInky = None
        self.iVecToPinky = None
        self.iVecToClyde = None
        self.iVecToBlinky = None
        self.vecToNearestGhost = None
    
    def updateDistsToGhosts(self):
        self.distFromPinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.pinky.position)
        self.distFromInky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.inky.position)
        self.distFromClyde = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.clyde.position)
        self.distFromBlinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.blinky.position)
    
    def updateVectorsFromGhostsToPac(self):
        self.vecToPinky = self.gc.pacman.position.__sub__(self.gc.ghosts.pinky.position)
        self.vecToInky = self.gc.pacman.position.__sub__(self.gc.ghosts.inky.position)
        self.vecToClyde = self.gc.pacman.position.__sub__(self.gc.ghosts.clyde.position)
        self.vecToBlinky = self.gc.pacman.position.__sub__(self.gc.ghosts.blinky.position)

    def updateVectorClosestPellet(self):
        closest_pellet = None
        min_pellet_dis = 10e10

        for pellet in self.gc.pellets.pelletList:
            dManhattan = self.gc.pacman.position.manhattanDistTo(pellet.position)
            if dManhattan < min_pellet_dis:
                min_pellet_dis = dManhattan
                closest_pellet = pellet

        self.vecToPellet = closest_pellet.position - self.gc.pacman.position
        self.vecToPellet /= self.vecToPellet.magnitude()

    def updateVectorClosestPowerPellet(self):
        closest_power_pellet = None
        min_power_pellet_dis = 10e10

        for pellet in self.gc.pellets.powerpellets:
            dManhattan = self.gc.pacman.position.manhattanDistTo(pellet.position)
            if dManhattan < min_power_pellet_dis:
                min_power_pellet_dis = dManhattan
                closest_power_pellet = pellet

        self.vecToPowerPellet = closest_power_pellet.position - self.gc.pacman.position
        self.vecToPowerPellet /= self.vecToPowerPellet.magnitude()

    def printGhostsPositions(self):
        print(f"PINKY POS: {self.gc.ghosts.pinky.position}")
        print(f"INKY POS: {self.gc.ghosts.inky.position}")
        print(f"CLYDE POS: {self.gc.ghosts.clyde.position}")
        print(f"BLINKY POS: {self.gc.ghosts.blinky.position}")

    def printDistToGhosts(self):
        print(f"DIST FROM PINKY: {self.distFromPinky}")
        print(f"DIST FROM INKY: {self.distFromInky}")
        print(f"DIST FROM CLYDE: {self.distFromClyde}")
        print(f"DIST FROM BLINKY: {self.distFromBlinky}")

    def printVectorsToPac(self):
        print(f"VECTOR TO PINKY: {self.vecToPinky}")
        print(f"VECTOR TO INKY: {self.vecToInky}")
        print(f"VECTOR TO CLYDE: {self.vecToClyde}")
        print(f"VECTOR TO BLINKY: {self.vecToBlinky}")

    def updateInverseGhostsVectors(self):
        self.iVecToInky = self.vecToInky.normalized() * (100/self.distFromInky)
        self.iVecToPinky = self.vecToPinky.normalized() * (100/self.distFromPinky)
        self.iVecToClyde = self.vecToClyde.normalized() * (100/self.distFromClyde)
        self.iVecToBlinky = self.vecToBlinky.normalized() * (100/self.distFromBlinky)
    
    def updateNearestGhost(self):
        min_distance = min([self.distFromBlinky,self.distFromClyde,self.distFromInky,self.distFromPinky])

        for ghost in self.gc.ghosts:
            ghost_distance = self.gc.pacman.position.manhattanDistTo(ghost.position)
            if (ghost_distance == min_distance):
                self.vecToNearestGhost = ghost.position.__sub__(self.gc.pacman.position)
    
    def updateResultantVecFromGhosts(self):
        self.resultantGhostVec = self.iVecToBlinky + self.iVecToInky + self.iVecToPinky + self.iVecToClyde

    def updateFinalResultantVector(self):
        self.finalResultantVec = self.resultantGhostVec + self.vecToPellet
    
    def updatePowerPelletsAvailability(self):
        self.powerPelletsAvailable = True if self.gc.pellets.powerpellets != [] else False

    def updatePowerModeStatus(self):
        self.powerMode = False
        for ghost in self.gc.ghosts:
            if ghost.mode.current == FREIGHT:
                self.powerMode = True
        
    def update(self):
        self.updateDistsToGhosts()
        self.updateVectorsFromGhostsToPac()
        self.updateInverseGhostsVectors()
        self.updateVectorClosestPellet()
        self.updateVectorClosestPowerPellet()
        self.updateNearestGhost()
        self.updateResultantVecFromGhosts()
        self.updateFinalResultantVector()
        self.updatePowerPelletsAvailability()
        self.updatePowerModeStatus()
    