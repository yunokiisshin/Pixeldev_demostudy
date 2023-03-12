import pygame 

###########################
# this is a class for weapons.
# 
class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
     
        # basic setup
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		# graphic
		full_path = f'./levelgraphics/graphics/weapons/{player.weapon}/{direction}.png'  # getting the path to indiv graphics
		self.image = pygame.image.load(full_path).convert_alpha()
		
		# placement
		if direction == 'right':
			self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))