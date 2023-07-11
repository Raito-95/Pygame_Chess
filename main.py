import sys
import pygame
import pygame.mixer as mixer
from menu import Menu
from game import Game
from constants import SCREEN_SIZE


def run_menu(screen):
    mixer.music.load('music/background.mp3')
    mixer.music.play(-1)

    menu = Menu(screen)

    while True:
        if menu.handle_events():
            break

        menu.draw()


def main():
    pygame.init()

    icon = pygame.image.load('image/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Chess Game')
    screen = pygame.display.set_mode(SCREEN_SIZE)

    run_menu(screen)

    game = Game(screen)
    game.change_music('music/fighting.mp3')
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
