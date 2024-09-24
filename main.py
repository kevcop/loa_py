# Importing the pygame library to manage game visuals and event handling
import pygame

# Importing the Game class to manage the gameplay
from game import Game

# Importing the Menu class to manage the initial game menu
from menu import Menu


# Main function to run the Lines of Action game
def main():
    # Initialize the pygame module
    pygame.init()

    # Create a window of size 800x800 pixels for the game
    window = pygame.display.set_mode((800, 800))

    # Set the caption of the window to "Lines of Action"
    pygame.display.set_caption("Lines of Action")

    # Initialize the menu object with the game window
    menu = Menu(window)

    # Initialize the game object as None; it will be created after menu interaction
    game = None

    # Boolean variable to keep the main game loop running
    running = True

    # Boolean variable to track whether the player is in the menu or the game
    in_menu = True

    # Main game loop
    while running:
        # Process each event in the pygame event queue
        for event in pygame.event.get():
            # If the event is quitting the game (close window), stop the loop
            if event.type == pygame.QUIT:
                running = False

            # If the left mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # If the player is in the menu
                if in_menu:
                    # Handle menu interactions based on the mouse click position
                    menu.handle_click(event.pos)

                    # If the player selected to load a saved game
                    if menu.selection_phase == "load_game":
                        # Start the loaded game with the provided settings
                        game_settings = menu.start_loaded_game()
                    else:
                        # Start a new game with the settings chosen in the menu
                        game_settings = menu.start_game()

                    # If valid game settings are provided, initialize the game
                    if game_settings:
                        print(f"Starting game with settings: {game_settings}")
                        # Switch to game mode, exiting the menu
                        in_menu = False

                        # Create the Game object using the settings from the menu
                        game = Game(
                            window,  # Pass the game window
                            game_settings['num_players'],  # Number of players
                            game_settings['players_type'],  # Type of players (human/computer)
                            game_settings['player_order'],  # Order of players
                            game_settings['player_colors'],  # Colors assigned to players
                            game_settings['board_size'],  # Size of the game board
                            game_settings.get('player_color'),  # Player color (optional)
                            game_settings.get('computer_color'),  # Computer color (optional)
                            game_settings.get('case')  # Pass the case if loading a saved game
                        )
                # If the player is in the game
                elif game:
                    # Handle mouse clicks during gameplay, passing click position to the game
                    game.handle_click(event.pos)

        # If the player is in the menu, display the menu
        if in_menu:
            menu.display()

        # If the player is in the game, update the game state and visuals
        elif game:
            game.update()

        # Update the entire pygame display after the menu or game has been updated
        pygame.display.flip()

    # When the main loop exits, quit pygame
    pygame.quit()


# Entry point of the script, calling the main function
if __name__ == "__main__":
    main()
