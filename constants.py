import pygame

SCREEN_SIZE = (1000, 640)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
LIGHT_BLUE = (180, 255, 255)

BUTTON_WIDTH_RATIO = 0.15
BUTTON_HEIGHT_RATIO = 0.065
BUTTON_SPACING_RATIO = 0.1
FONTS_SIZE = int(SCREEN_SIZE[1] * 0.05)

BUTTON_WIDTH = int(SCREEN_SIZE[0] * BUTTON_WIDTH_RATIO)
BUTTON_HEIGHT = int(SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO)

piece_images = {}
pieces = {
    'white_pawn':   ('white', 'pawn'),
    'white_rook':   ('white', 'rook'),
    'white_knight': ('white', 'knight'),
    'white_bishop': ('white', 'bishop'),
    'white_queen':  ('white', 'queen'),
    'white_king':   ('white', 'king'),
    'black_pawn':   ('black', 'pawn'),
    'black_rook':   ('black', 'rook'),
    'black_knight': ('black', 'knight'),
    'black_bishop': ('black', 'bishop'),
    'black_queen':  ('black', 'queen'),
    'black_king':   ('black', 'king')
}

for key, (color, name) in pieces.items():
    piece_images[key] = pygame.image.load(f"image/{color}_{name}.png")

