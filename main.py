# main.py

import pygame
from game import Game
from menu import Menu

def main():
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lines of Action")

    menu = Menu(window)
    game = None

    running = True
    in_menu = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if in_menu:
                    menu.handle_click(event.pos)
                    if menu.start_game():  # Check if the game should start
                        in_menu = False
                        # Now we can start the game with the chosen players
                        game = Game(window, menu.num_players, menu.players_type)
                elif game:
                    game.handle_click(event.pos)

        if in_menu:
            menu.display()
        elif game:
            game.update()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
