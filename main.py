import pygame
from menu import Menu
from game import Game

def main():
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Lines of Action")

    # Initialize the menu and display it
    menu = Menu(window)

    running = True
    while running:
        menu.display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu.handle_click(event.pos)

        # Check if the game should start
        if menu.start_game():
            # Pass player and computer colors along with other parameters
            game = Game(window, menu.num_players, menu.players_type, menu.board_size, menu.player_color, menu.computer_color)
            running = False

    # Now start the game loop
    game_running = True
    while game_running:
        game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
