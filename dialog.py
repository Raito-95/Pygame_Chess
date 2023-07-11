import pygame
from constants import SCREEN_SIZE, FONTS_SIZE, BUTTON_SPACING_RATIO, GRAY, LIGHT_GRAY, BLACK, BUTTON_WIDTH, BUTTON_HEIGHT
from typing import Optional, List


class Dialog:
    def __init__(self, screen):
        self.screen = screen

        self.button_spacing = int(SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)

        self.dialog_font = pygame.font.SysFont("Script MT Bold", FONTS_SIZE)
        self.start_x = int((SCREEN_SIZE[0] // 2) - (BUTTON_WIDTH // 2))
        self.start_y = int((SCREEN_SIZE[1] // 2) - (BUTTON_HEIGHT // 2))

    def draw_button(self, rect, text, hover=False):
        color = LIGHT_GRAY if hover else GRAY
        pygame.draw.rect(self.screen, color, rect)

        text_surface = self.dialog_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_option_buttons(self, options, mouse_pos):
        option_rects = []
        for idx, option in enumerate(options):
            button_rect = pygame.Rect(
                self.start_x, self.start_y + self.button_spacing * idx, BUTTON_WIDTH, BUTTON_HEIGHT)
            is_hover = button_rect.collidepoint(mouse_pos)
            self.draw_button(button_rect, option['label'], is_hover)

            option['rect'] = button_rect
            option_rects.append(button_rect)
        return option_rects

    def show_message(self, message, options=None) -> Optional[str]:
        option_rects: List[pygame.Rect] = []
        text_surface = self.dialog_font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.screen.blit(text_surface, text_rect)

        if options is not None:
            mouse_pos = pygame.mouse.get_pos()
            option_rects = self.draw_option_buttons(options, mouse_pos)

        pygame.display.flip()

        while options is not None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for option, rect in zip(options, option_rects):
                            if rect.collidepoint(event.pos):
                                return option['action']
                elif event.type == pygame.QUIT:
                    return None

    def show_promotion(self, x, y, board):
        dialog = "Select a piece to promote to:"
        options = [
            {"label": "Rook", "action": "rook"},
            {"label": "Knight", "action": "knight"},
            {"label": "Bishop", "action": "bishop"},
            {"label": "Queen", "action": "queen"},
        ]
        action = self.show_message(dialog, options)
        if action:
            board.promote_pawn(x, y, action)

    def show_proposal(self):
        dialog = "Your opponent has offered a draw. Do you accept?"
        options = [
            {"label": "Accept", "action": "accept"},
            {"label": "Decline", "action": "decline"},
        ]
        action = self.show_message(dialog, options)
        if action == "accept":
            return True
        else:
            return False
