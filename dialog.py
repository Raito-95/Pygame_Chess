import pygame
from constants import SCREEN_SIZE, BUTTON_WIDTH_RATIO, BUTTON_HEIGHT_RATIO, BUTTON_SPACING_RATIO, FONTS_SIZE


class Dialog:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.fonts = {}

    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size]

    def render_text(self, text, size, color):
        font = self.get_font(size)
        text_surface = font.render(text, True, color)
        return text_surface

    def draw_button(self, overlay, rect, text, text_color, bg_color):
        pygame.draw.rect(overlay, bg_color, rect)
        label = self.render_text(text, FONTS_SIZE, text_color)
        overlay.blit(label, label.get_rect(center=rect.center))

    def draw_option_buttons(self, options, start_x, start_y, button_width, button_height, spacing):
        for idx, option in enumerate(options):
            button_rect = pygame.Rect(start_x, start_y + spacing * idx, button_width, button_height)
            self.draw_button(self.overlay, button_rect, option['label'], (0, 0, 0), (255, 255, 255))
            option['rect'] = button_rect

    def show_message(self, message, options=None):
        self.overlay.fill((0, 0, 0, 128))

        if options is not None:
            button_width = int(SCREEN_SIZE[0] * BUTTON_WIDTH_RATIO)
            button_height = int(SCREEN_SIZE[1] * BUTTON_HEIGHT_RATIO)
            button_spacing = int(SCREEN_SIZE[1] * BUTTON_SPACING_RATIO)

            start_x = int((SCREEN_SIZE[0] // 2) - (button_width // 2))
            start_y = int((SCREEN_SIZE[1] // 2) - (button_height + (button_spacing // 2)))

            self.draw_option_buttons(options, start_x, start_y, button_width, button_height, button_spacing)

        text_surface = self.render_text(message, FONTS_SIZE, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        self.overlay.blit(text_surface, text_rect)

        self.screen.blit(self.overlay, (0, 0))
        pygame.display.flip()

        if options is not None:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for option in options:
                                if option['rect'].collidepoint(event.pos):
                                    return option['action']
                    elif event.type == pygame.QUIT:
                        return None

    def show_promotion_dialog(self, x, y, board):
        options = [
            {"label": "Rook", "action": "rook"},
            {"label": "Knight", "action": "knight"},
            {"label": "Bishop", "action": "bishop"},
            {"label": "Queen", "action": "queen"},
        ]

        action = self.show_message("Select a piece to promote to:", options)
        if action:
            board.promote_pawn(x, y, action)

    def show_draw_offer_dialog(self):
        prompt = "Your opponent has offered a draw. Do you accept?"
        options = [
            {"label": "Accept", "action": "accept"},
            {"label": "Decline", "action": "decline"},
        ]

        action = self.show_message(prompt, options)

        return action == "accept"