import pygame

SCREEN_SIZE = (1000, 640)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
LIGHT_BLUE = (181, 255, 255)

piece_images = {}
pieces = {
    'white_pawn': ('white', 'pawn'),
    'white_rook': ('white', 'rook'),
    'white_knight': ('white', 'knight'),
    'white_bishop': ('white', 'bishop'),
    'white_queen': ('white', 'queen'),
    'white_king': ('white', 'king'),
    'black_pawn': ('black', 'pawn'),
    'black_rook': ('black', 'rook'),
    'black_knight': ('black', 'knight'),
    'black_bishop': ('black', 'bishop'),
    'black_queen': ('black', 'queen'),
    'black_king': ('black', 'king')
}

for key, (color, name) in pieces.items():
    piece_images[key] = pygame.image.load(f"image/{color}_{name}.png")
