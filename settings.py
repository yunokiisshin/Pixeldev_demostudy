import pygame

# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './levelgraphics/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18


# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# UI colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'


# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'./levelgraphics/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'./levelgraphics/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'./levelgraphics/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'./levelgraphics/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'./levelgraphics/graphics/weapons/sai/full.png'}}


# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'./levelgraphics/graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'./levelgraphics/graphics/particles/heal/heal.png'}}