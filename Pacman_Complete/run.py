# Python libs
import pygame, sys
from pygame.locals import *
import json
sys.path.append("../")

# Pacman libs
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData

# GA libs
from GA.GeneticManager import GeneticManager
from GA.PopulationManager import PopulationManager
from GA.Individual import Individual
from Pacman_Complete.params_reader import POPULATION, RUN, INDIVIDUAL
from Useful_information.Useful_information import UsefulInformation
from Metrics.GenerationsMetrics import *

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(False)
        self.pause.setPause(pauseTime=5)
        self.level = 0
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

        self.pacmanSkipFrames = 25
        self.pacmanSkipedFrames = 0
        self.currVecToFollow = None

    def startGame_old(self):      
        self.mazedata.loadMaze(self.level)#######
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze1.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    def update(self, vecToFollow):
        dt = self.clock.tick(240) / 125.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        finalScore = None
        if not self.pause.paused:
            self.ghosts.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            finalScore = self.checkGhostEvents()
        
        # Prevents pacman flickering
        if  self.pacmanSkipedFrames <= 0:
            self.pacmanSkipedFrames = self.pacmanSkipFrames
            self.currVecToFollow = vecToFollow
        else:
            self.pacmanSkipedFrames -= 1


        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt, self.currVecToFollow)
        else:
            self.pacman.update(dt, self.currVecToFollow)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if not self.pause.paused:
            self.textgroup.hideText()
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()
        
        return finalScore

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            #self.hideEntities()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.printScore)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)                  
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=1, func=self.restartGame)
                            return self.score
                        else:
                            self.pause.setPause(pauseTime=1, func=self.resetLevel)
        return None
    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                # print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = False
        self.pause.setPause(pauseTime=5)
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = False
        self.pause.setPause(pauseTime=5)
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)
    
    def printScore(self):
        print(f"SCORE: {self.score}")

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


def playIndividual(ind, game, useful_info):
    game.startGame()
    finalScore = None
    while True:
        useful_info.update()
        rna = useful_info.current_rna()
        action = ind.get_action(rna)
        finalScore = game.update(action)
        if (finalScore):
            ind.set_fitness(finalScore)
            break

def saveBestIndividual(population, data_dir_path):
    best_individual = max(population,key=lambda x : x.get_fitness())
    best_dna = best_individual.get_dna()
    file_path = os.path.join(data_dir_path,f"best.pacw")

    with open(file_path, "w") as file: 
        file_txt = json.dumps(best_dna) 
        file.write(file_txt) 
    
    print(f"Best individual weights saved at {file_path}!")

def main():
    game = GameController()
    useful_info = UsefulInformation(game)

    # If weights are given, play the individual with these weights
    print(INDIVIDUAL)
    if INDIVIDUAL != {}:
        print("Running given individual")
        ind = Individual(INDIVIDUAL)
        playIndividual(ind, game, useful_info)
        game.printScore()
        return

    # If weights are not given, runs the GA

    gm = GeneticManager()

    pm = PopulationManager()
    pm.init_population()
    population = pm.get_population()
    generation_metrics = GenerationsMetrics()

    curr_datetime = datetime.now().strftime('%m_%d_%H_%M_%S')
    data_dir_path = os.path.join(os.getcwd(),'data',f'{curr_datetime}')
    os.makedirs(data_dir_path, exist_ok=True)

    for i in range(len(population)):
        ind = population[i]
        print(f"Individual: {i}")
        playIndividual(ind, game, useful_info)
        print(f"FITNESS: {ind.get_fitness()}")

    iter = 0

    # early stopping vars
    no_increase_iters = 0
    prev_avg_fitness = 0
    max_reached = False
    
    population_fitness = [pop.get_fitness() for pop in population]
    avg_fit, std_fit, best_fit = generation_metrics.calculate_metrics(population_fitness)

    while iter < RUN['iterations']:
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print(f"Iteration: {iter}")
        print('---------------------')

        population = pm.get_population()

        for i in range(len(population)):
            ind = population[i]
            print(f"Individual: {i}")
            print(f"FITNESS: {ind.get_fitness()}")

        population_fitness = [pop.get_fitness() for pop in population]
        print(f"Gen {iter}> AVG: {avg_fit:3f} | STD: {std_fit:3f} | BEST: {best_fit}")
        
        
        if prev_avg_fitness < avg_fit:
            no_increase_iters = 0
        else:
            no_increase_iters += 1
            if no_increase_iters == RUN['early_stopping_max_iters']:
                break

        for fit in population_fitness:
            if fit >= 5800:
                max_reached = True

        if max_reached:
            saveBestIndividual(pm.get_population(), data_dir_path)
            break

        parents = pm.tournament()
        offspring = gm.crossover(parents)
        mutated_offspring = gm.mutation(offspring)

        for ind in mutated_offspring:
            print(f"New Individual: ")
            playIndividual(ind, game, useful_info)
            print(f"FITNESS: {ind.get_fitness()}")

        if POPULATION['survival'] == 'elitist':
            pm.survival_elitist(mutated_offspring)
        elif POPULATION['survival'] == 'replace':
            pm.survival_replace(parents, mutated_offspring)
        
        population_fitness = [pop.get_fitness() for pop in population]
        avg_fit, std_fit, best_fit = generation_metrics.calculate_metrics(population_fitness)

        if prev_avg_fitness < avg_fit:
            no_increase_iters = 0
        else:
            no_increase_iters += 1
            print(f"Patience: {no_increase_iters}/{RUN['early_stopping_max_iters']}")
            if no_increase_iters == RUN['early_stopping_max_iters']:
                print("Early stop")
                break

        for fit in population_fitness:
            if fit >= 5800:
                max_reached = True

        if max_reached:
            saveBestIndividual(pm.get_population(), data_dir_path)
            break
        
        prev_avg_fitness = avg_fit
        saveBestIndividual(pm.get_population(), data_dir_path)
        
        iter += 1

    
    avg_avg_fit, avg_std_fit, best_fit_exe = generation_metrics.get_execution_metrics()
    print(f"EXE METRICS> AVG: {avg_avg_fit:3f} | STD: {avg_std_fit:3f} | BEST: {best_fit_exe}")
    generation_metrics.save_statistic(data_dir_path, iter)


if __name__ == "__main__":
    main()



