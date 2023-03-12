import pygame 
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


##############################
# This class represents the game session.
class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

		# user interface 
		self.ui = UI()	# initialize UI
		self.upgrade = Upgrade(self.player)

		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

	#####
	# this function creates the map from the layout made by Tiled.
	def create_map(self):
		layouts = {		# this is the visible layout of several items/layers
			'boundary': import_csv_layout('./levelgraphics/map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('./levelgraphics/map/map_Grass.csv'),
			'object': import_csv_layout('./levelgraphics/map/map_Objects.csv'),
			'entities': import_csv_layout('./levelgraphics/map/map_Entities.csv')
		}	# style: layout
		graphics = {	# responsible for putting graphics on
			'grass': import_folder('./levelgraphics/graphics/Grass'),
			'objects': import_folder('./levelgraphics/graphics/objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):	# looking through each grid(tile) of the map
					if col != '-1':		# col number is related to the individual item placed at that coordinate
						
						# current coordinates
						x = col_index * TILESIZE
						y = row_index * TILESIZE
      
						# sets invisible boundary
						if style == 'boundary':		
							Tile((x,y),[self.obstacle_sprites],'invisible')
						
						# places grass with random graphics
						if style == 'grass':		
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
								'grass',
								random_grass_image)
						
      					# places objects on map
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						# places entities (player, enemy) on map
						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x,y),
									[self.visible_sprites],
									self.obstacle_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic)
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name ='raccoon'
								else: monster_name = 'squid'
								Enemy(
									monster_name,
									(x,y),
									[self.visible_sprites,self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp)

	# create weapon attack instance
	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

	# create magic attack instance
	def create_magic(self,style,strength,cost):	# changes based on magic type
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

	# ends attack
	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None
  
	# deals with attacking with damageable player moves
	def player_attack_logic(self):
		if self.attack_sprites:		
			for attack_sprite in self.attack_sprites:	# loops through all attacks (weapon, fire)
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:	# checking with collision with all attackable sprites
					for target_sprite in collision_sprites:
						# dealing with grass destruction
						if target_sprite.sprite_type == 'grass': 
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	# calculate the damage the player took
	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	# death particle articulation
	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	# adds exp by amount
	def add_exp(self,amount):
		self.player.exp += amount

	# pauses the screen
	def toggle_menu(self):
		self.game_paused = not self.game_paused 

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		
  		# displays menu if the game is paused (after toggle_menu)
		if self.game_paused:
			self.upgrade.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
		
##############################
# This class customizes the camera and the groupings.
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('./levelgraphics/graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	# handles enemy sprite update
	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
