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
                    game_settings = menu.start_game()
                    if game_settings:
                        print(f"Starting game with settings: {game_settings}")# Check if we have transitioned to the game
                        in_menu = False
                        game = Game(
                            window,
                            game_settings['num_players'],
                            game_settings['players_type'],
                            game_settings['player_order'],
                            game_settings['player_colors'],
                            game_settings['board_size'],
                            game_settings.get('player_color'),
                            game_settings.get('computer_color')
                        )
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
