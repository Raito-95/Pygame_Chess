import sys
import pygame
import pygame.mixer as mixer
from menu import Menu
from game import Game
from constants import SCREEN_SIZE


def main():
    icon_surface = pygame.image.load('image/icon.png')

    pygame.init()

    pygame.display.set_icon(icon_surface)
    pygame.display.set_caption('Chess Game')
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.set_alpha(None)

    # mixer.music.load('music/background.mp3')
    # mixer.music.play(-1)

    menu = Menu(screen)

    while True:
        if menu.handle_events():
            break

        menu.draw()

    game = Game(screen)
    # game.change_music('music/fighting.mp3')
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
