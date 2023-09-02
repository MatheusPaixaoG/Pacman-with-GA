class UsefulInformation():
    def __init__(self, game_controller):
        self.gc = game_controller

        self.iVecToInky = None
        self.iVecToPinky = None
        self.iVecToClyde = None
        self.iVecToBlinky = None
    
    def updateDistsToGhosts(self):
        self.distFromPinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.pinky.position)
        self.distFromInky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.inky.position)
        self.distFromClyde = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.clyde.position)
        self.distFromBlinky = self.gc.pacman.position.manhattanDistTo(self.gc.ghosts.blinky.position)
    
    def updateVectorsFromGhostsToPac(self):
        self.vecToPinky = self.gc.ghosts.pinky.position.__sub__(self.gc.pacman.position)
        self.vecToInky = self.gc.ghosts.inky.position.__sub__(self.gc.pacman.position)
        self.vecToClyde = self.gc.ghosts.clyde.position.__sub__(self.gc.pacman.position)
        self.vecToBlinky = self.gc.ghosts.blinky.position.__sub__(self.gc.pacman.position)

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

    def inverseGhostsVectors(self):
        pacVectorNormalized = self.gc.pacman.position.normalized
        self.iVecToInky = pacVectorNormalized * (1/self.distFromInky)
        self.iVecToPinky = pacVectorNormalized * (1/self.distFromPinky)
        self.iVecToClyde = pacVectorNormalized * (1/self.distFromClyde)
        self.iVecToBlinky = pacVectorNormalized * (1/self.distFromBlinky)
        
    def update(self):
        self.updateDistsToGhosts()
        self.updateVectorsFromGhostsToPac()