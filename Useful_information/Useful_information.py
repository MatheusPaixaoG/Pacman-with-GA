class UsefulInformation():
    def __init__(self, game_controller):
        self.gc = game_controller
    
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
    
    def updateDistsToGhosts(self):
        self.distFromPinky = self.gc.pacman.position.distTo(self.gc.ghosts.pinky.position)
        self.distFromInky = self.gc.pacman.position.distTo(self.gc.ghosts.inky.position)
        self.distFromClyde = self.gc.pacman.position.distTo(self.gc.ghosts.clyde.position)
        self.distFromBlinky = self.gc.pacman.position.distTo(self.gc.ghosts.blinky.position)
        
    def update(self):
        self.updateDistsToGhosts()