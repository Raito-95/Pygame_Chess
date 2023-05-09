import sys
import pygame
from constants import SCREEN_SIZE, FONTS_SIZE, BUTTON_SPACING_RATIO


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont(None, FONTS_SIZE*2.5)
        self.menu_font = pygame.font.SysFont(None, FONTS_SIZE*1.5)
        self.options = [
            'NEW GAME',
            'EXIT'
        ]
        self.background_image = pygame.image.load('image/menu_background.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, SCREEN_SIZE)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        title_text = self.title_font.render('CHESS GAME', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 3))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            option_text = self.menu_font.render(option, True, (255, 255, 255))
            option_rect = option_text.get_rect(
                center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + i * (SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.options):
                        option_text = self.menu_font.render(option, True, (0, 0, 0))
                        option_rect = option_text.get_rect(
                            center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + i * (SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)))
                        if option_rect.collidepoint(mouse_pos):
                            if i == 0:
                                return True
                            elif i == 1:
                                pygame.quit()
                                sys.exit()

        return False
