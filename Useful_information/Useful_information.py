import sys
sys.path.append("../")

from Pacman_Complete.constants import *

class UsefulInformation():
    def __init__(self, game_controller):
        self.gc = game_controller

        self.powerMode = False
        self.powerPelletsAvailable = False

        self.resultantGhostVec = None
        self.vecToNearestGhost = None
    
    def calculateDistsToGhosts(self):
        distFromPinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.pinky.position)
        distFromInky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.inky.position)
        distFromClyde = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.clyde.position)
        distFromBlinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.blinky.position)
        return distFromPinky, distFromInky, distFromClyde, distFromBlinky
    
    def calculateVectorsFromGhostsToPac(self):
        vecToPinky = self.gc.pacman.position.__sub__(self.gc.ghosts.pinky.position)
        vecToInky = self.gc.pacman.position.__sub__(self.gc.ghosts.inky.position)
        vecToClyde = self.gc.pacman.position.__sub__(self.gc.ghosts.clyde.position)
        vecToBlinky = self.gc.pacman.position.__sub__(self.gc.ghosts.blinky.position)
        return vecToPinky, vecToInky, vecToClyde, vecToBlinky

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
        distToPinky, distToInky, distToClyde, distToBlinky = self.calculateDistsToGhosts()
        print(f"DIST FROM PINKY: {distToPinky}")
        print(f"DIST FROM INKY: {distToInky}")
        print(f"DIST FROM CLYDE: {distToClyde}")
        print(f"DIST FROM BLINKY: {distToBlinky}")

    def printVectorsToPac(self):
        vecToPinky, vecToInky, vecToClyde, vecToBlinky = self.calculateVectorsFromGhostsToPac()
        print(f"VECTOR TO PINKY: {vecToPinky}")
        print(f"VECTOR TO INKY: {vecToInky}")
        print(f"VECTOR TO CLYDE: {vecToClyde}")
        print(f"VECTOR TO BLINKY: {vecToBlinky}")

    def calculateInverseGhostsVectors(self):
        # Calculate requirements
        distToPinky, distToInky, distToClyde, distToBlinky = self.calculateDistsToGhosts()
        vecToPinky, vecToInky, vecToClyde, vecToBlinky = self.calculateVectorsFromGhostsToPac()

        # Calculate inverse vectors
        iVecToInky = vecToInky.normalized() * (100/distToInky)
        iVecToPinky = vecToPinky.normalized() * (100/distToPinky)
        iVecToClyde = vecToClyde.normalized() * (100/distToClyde)
        iVecToBlinky = vecToBlinky.normalized() * (100/distToBlinky)
        return iVecToPinky, iVecToInky, iVecToClyde, iVecToBlinky
    
    def updateNearestGhost(self):
        distsTuple = self.calculateDistsToGhosts()
        min_distance = min(distsTuple)

        for ghost in self.gc.ghosts:
            ghost_distance = self.gc.pacman.position.manhattanDistTo(ghost.position)
            if (ghost_distance == min_distance):
                self.vecToNearestGhost = ghost.position.__sub__(self.gc.pacman.position)
    
    def updateResultantVecFromGhosts(self):
        iVecToPinky, iVecToInky, iVecToClyde, iVecToBlinky = self.calculateInverseGhostsVectors()
        self.resultantGhostVec = iVecToBlinky + iVecToInky + iVecToPinky + iVecToClyde

    def updateFinalResultantVector(self):
        self.finalResultantVec = self.resultantGhostVec + self.vecToPellet
    
    def updatePowerPelletsAvailability(self):
        self.powerPelletsAvailable = False
        for pp in self.gc.pellets.powerpellets:
            if pp.visible:
                self.powerPelletsAvailable = True

    def updatePowerModeStatus(self):
        self.powerMode = False
        for ghost in self.gc.ghosts:
            if ghost.mode.current == FREIGHT:
                self.powerMode = True
        
    def update(self):
        self.updateVectorClosestPellet()
        self.updateVectorClosestPowerPellet()
        self.updateNearestGhost()
        self.updateResultantVecFromGhosts()
        self.updatePowerPelletsAvailability()
        self.updatePowerModeStatus()
    
    def current_rna(self):
        return {
            "Vector2": [
                self.vecToPellet,               # nearest_pellet
                self.vecToPowerPellet,          # nearest_food
                self.resultantGhostVec,         # distance_ghosts
                self.vecToNearestGhost          # nearest_ghost
            ],
            "bool": [
                self.powerMode,                 # super_mode (bool)
                self.powerPelletsAvailable,     # exist_food (bool)
            ]
        }