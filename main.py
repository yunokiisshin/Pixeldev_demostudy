import pygame, sys
from settings import *
from level import Level

#################################
# This class represents a round of game, containing pygame setups
class Game:
    def __init__(self):
        
        #initial setup; booting, naming, and setting screen & clock
        pygame.init()
        pygame.display.set_caption('Pixeladv')
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('white')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()