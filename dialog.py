import pygame
from constants import SCREEN_SIZE, BUTTON_WIDTH_RATIO, BUTTON_HEIGHT_RATIO, BUTTON_SPACING_RATIO, FONTS_SIZE, GRAY, BLACK


class Dialog:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.dialog_font = pygame.font.SysFont(None, FONTS_SIZE)
        self.button_width = int(SCREEN_SIZE[0] * BUTTON_WIDTH_RATIO)
        self.button_height = int(SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO)
        self.button_spacing = int(SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)

        self.start_x = int((SCREEN_SIZE[0] // 2) - (self.button_width // 2))
        self.start_y = int((SCREEN_SIZE[1] // 2) - (self.button_height // 2))

    def draw_option_buttons(self, options):
        option_rects = []
        for idx, option in enumerate(options):
            button_rect = pygame.Rect(
                self.start_x, self.start_y + self.button_spacing * idx, self.button_width, self.button_height)
            pygame.draw.rect(self.overlay, GRAY, button_rect)

            # text_surface = self.dialog_font.render(option['label'], True, BLACK)
            # text_rect = text_surface.get_rect(center=button_rect.center)
            # self.overlay.blit(text_surface, text_rect)

            option['rect'] = button_rect
            option_rects.append(button_rect)
        return option_rects

    def show_message(self, message, options=None):
        self.overlay.fill((0, 0, 0, 128))
        text_surface = self.dialog_font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.overlay.blit(text_surface, text_rect)
        
        if options is not None: 
            option_rects = self.draw_option_buttons(options)

        self.screen.blit(self.overlay, (0, 0))
        pygame.display.flip()
        
        if options is not None: 
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for option, rect in zip(options, option_rects):
                                if rect.collidepoint(event.pos):
                                    return option['action']
                    elif event.type == pygame.QUIT:
                        return None

    def show_promotion(self, x, y, board):
        print('show_promotion')
        dialog = "Select a piece to promote to:"
        options = [
            {"label": "Rook", "action": "rook"},
            {"label": "Knight", "action": "knight"},
            {"label": "Bishop", "action": "bishop"},
            {"label": "Queen", "action": "queen"},
        ]
        print('test1')
        action = self.show_message(dialog, options)
        if action:
            board.promote_pawn(x, y, action)

    def show_proposal(self):
        print('show_proposal')
        dialog = "Your opponent has offered a draw. Do you accept?"
        options = [
            {"label": "Accept", "action": "accept"},
            {"label": "Decline", "action": "decline"},
        ]
        print('test2')
        action = self.show_message(dialog, options)

        return action == "accept"