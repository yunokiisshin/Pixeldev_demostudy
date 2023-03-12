import pygame, sys
from settings import *
from level import Level


##############################
# This class represents the game session.
class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))	# sets screen size from setting
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		# creates level
		self.level = Level()

		# sound
		main_sound = pygame.mixer.Sound('./levelgraphics/audio/main.ogg')
		main_sound.set_volume(0.5)	# controls main bgm volume
		main_sound.play(loops = -1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()