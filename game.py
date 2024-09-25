import pygame
from board import Board
from menu import Menu
from piece import Piece
from HumanPlayer import HumanPlayer
from computerPlayer import ComputerPlayer  # AI class
import os
import time


class Game:
    """
    Function Name: __init__
    Purpose: Initializes the game with the provided settings.
    Parameters:
        window (pygame.Surface): The game window.
        num_players (int): The number of players (2 or 4).
        players_type (list): List specifying whether each player is human or computer.
        player_order (list): The order in which players take turns (optional).
        player_colors (dict): A dictionary mapping player numbers to their colors (optional).
        board_size (int): The size of the board.
        player_color (tuple): RGB color of the player for 2-player mode.
        computer_color (tuple): RGB color of the computer for 2-player mode.
        case (int): The number of the saved game case (optional).
    Return Value: None
    Algorithm:
        1) Initialize game settings and variables.
        2) If a case is provided, load the saved game state; otherwise, reset the game.
    Reference: None
    """

    def __init__(self, window, num_players, players_type, player_order=None, player_colors=None, board_size=None,
                 player_color=None, computer_color=None, case=None):
        # Initialize the game window
        self.window = window

        # Number of players (either 2 or 4)
        self.num_players = num_players

        # List containing player types (Human or Computer)
        self.players_type = players_type

        # Define the order in which players will take turns, if provided
        self.player_order = player_order if player_order is not None else []

        # Dictionary mapping player numbers to their assigned colors
        self.player_colors = player_colors if player_colors is not None else {}

        # Size of the game board (e.g., 8x8, 12x12, etc.)
        self.board_size = board_size

        # The player's piece color for 2-player mode
        self.player_color = player_color

        # The computer's piece color for 2-player mode
        self.computer_color = computer_color

        # The piece currently selected by the player (None if no piece is selected)
        self.selected_piece = None

        # Variable to store any error messages (e.g., invalid moves)
        self.error_message = ""

        # A list to store the move history throughout the game
        self.move_history = []

        # Font used for displaying the move history
        self.history_font = pygame.font.SysFont('Arial', 20)

        # Height of the box that will display the move history
        self.history_box_height = 150

        # Padding within the move history box
        self.history_offset = 10

        # Rectangle defining the area for the "Show History" button
        self.show_history_button_rect = pygame.Rect(650, 20, 140, 50)

        # Rectangle defining the area for the "Save Game" button
        self.save_game_button_rect = pygame.Rect(650, 80, 140, 50)

        # Rectangle defining the area for the "Help" button
        self.help_button_rect = pygame.Rect(650, 140, 140, 50)

        # Flag to track if the winner has been displayed
        self.winner_displayed = False

        # A list to store the players (Human or AI)
        self.players = []

        # Track whose turn it is (starts with 0 for the first player)
        self.current_turn = 0

        # Dictionary to store the number of rounds won by each player
        self.player_wins = {i: 0 for i in range(self.num_players)}

        # Dictionary to store the scores for each player
        self.player_scores = {i: 0 for i in range(self.num_players)}

        # Track the color of the winner from the previous round (if applicable)
        self.previous_winner_color = None

        # Print debugging information about the number of players
        print(f"Initializing game with {num_players} players.")

        # If a saved game case is provided, load the game state from the file
        if case:
            self.load_game_state(case)
        else:
            # Otherwise, start a new game by resetting everything
            self.reset_game()


    """
    Function Name: reset_game
    Purpose: Resets all necessary game variables for a new round.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Reset the winner flag and initialize a new board.
        2) Recreate players for the new game.
        3) Clear move history and error messages.
        4) Ensure proper setup for the first turn based on the mode (2-player or 4-player).
    Reference: None
    """

    def reset_game(self):
        # Print debugging information indicating the game is resetting
        print("Resetting the game for a new round...")

        # Reset the flag indicating if the winner has been displayed
        self.winner_displayed = False
        print(f"Winner flag reset: {self.winner_displayed}")

        # Initialize a new board based on the specified board size
        self.board = Board(self.board_size)
        print("New board initialized with size", self.board_size)
        print(f"Board state after reset: {self.board.pieces}")

        # Reset selected piece, error messages, and move history
        self.selected_piece = None
        self.error_message = ""
        self.move_history = []

        # Recreate the players for the new game
        self.players = self.create_players()
        print(f"Players created: {self.players}")

        # Print debugging information about the number of players created
        print(f"Number of players: {len(self.players)}")
        if len(self.players) != self.num_players:
            print(f"Error: Expected {self.num_players} players but got {len(self.players)}")

        # Clear move history and reset error messages
        print("Move history cleared, and error messages reset.")

        # Set up the first turn depending on the game mode (2-player or 4-player)
        if self.num_players == 2:
            # Check if the player color needs to be swapped based on the previous winner
            if self.previous_winner_color == (255, 255, 255) and self.player_wins[0] != self.player_wins[1]:
                self.player_color, self.computer_color = self.computer_color, self.player_color
                print(f"Swapping colors. Player color: {self.get_color_name(self.player_color)}, "
                      f"Computer color: {self.get_color_name(self.computer_color)}")

            # Determine who moves first based on the color of the black pieces
            if self.player_color == (0, 0, 0):  # Black
                self.current_turn = 0  # Player moves first
                print("Player (Black) moves first.")
            else:
                self.current_turn = 1  # Computer moves first
                print("Computer (Black) moves first.")
        else:
            # In 4-player mode, determine which player is assigned to the black pieces
            black_player = [player for player, color in self.player_colors.items() if color == (0, 0, 0)][0]
            self.current_turn = black_player - 1  # Set the current turn to the player assigned to Black
            print(f"Player {black_player} (Black) moves first.")
    """
    Function Name: create_players
    Purpose: Creates the players for the game based on the number of players and their types.
    Parameters: None
    Return Value:
        list: A list of players (HumanPlayer or ComputerPlayer objects).
    Algorithm:
        1) Based on the number of players, create HumanPlayer or ComputerPlayer instances.
        2) Assign appropriate colors to each player.
        3) Return the list of created players.
    Reference: None
    """

    def create_players(self):
        # Initialize an empty list to hold the player objects
        players = []
        print("Creating players...")

        # If there are only 2 players, assign them colors and types (Human or Computer)
        if self.num_players == 2:
            colors = [self.player_color, self.computer_color]
            print(f"2-player game with colors: {colors}")
            for i in range(self.num_players):
                if self.players_type[i] == "Computer":
                    print(f"Player {i + 1} is a computer.")
                    players.append(ComputerPlayer(self.board, colors[i]))  # AI player
                else:
                    print(f"Player {i + 1} is a human.")
                    players.append(HumanPlayer())  # Human player

        # In 4-player mode, create players and assign them colors from the player_colors dictionary
        else:
            for i in range(1, self.num_players + 1):  # Use 1-based index for 4-player mode
                if self.players_type[i - 1] == "Computer":
                    print(f"Player {i} is a computer. Color: {self.player_colors[i]}")
                    players.append(ComputerPlayer(self.board, self.player_colors[i]))  # AI player
                else:
                    print(f"Player {i} is a human. Color: {self.player_colors[i]}")
                    players.append(HumanPlayer())  # Human player

        # Print debugging information about the created players
        print(f"Players created: {players}")
        return players

    """
    Function Name: update
    Purpose: Updates the game state and handles rendering.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Clear the screen and redraw the board.
        2) Display error messages, buttons, and check for a winner.
        3) If it's a computer player's turn, make a move automatically.
    Reference: Chatgpt
    """

    def update(self):
        # Print debugging information about the current state of the game
        print("Game update running...")  # Debugging
        print(f"Winner flag before update: {self.winner_displayed}")  # Debugging
        print(f"Current turn: {self.current_turn}")  # Debugging
        print(f"Current player: {type(self.players[self.current_turn])}")  # Debugging

        # Reset the winner display flag before the update
        self.winner_displayed = False

        # Fill the game window with a white background to clear any old content
        self.window.fill((255, 255, 255))

        # Draw the current state of the board and pieces
        self.board.draw(self.window, self.selected_piece)

        # Display any error messages on the screen
        self.display_error_message()

        # Show the "Show History" button on the screen
        self.display_show_history_button()

        # Show the "Save Game" button on the screen
        self.display_save_game_button()

        # Show the "Help" button on the screen
        self.display_help_button()

        # Display the current player's turn on the screen
        self.display_current_player()

        # Check if there is a winner; only check if the winner hasn't been displayed yet
        if not self.winner_displayed:
            print("Checking for a winner...")  # Debugging
            self.check_winner()
        else:
            print("Winner has already been displayed, skipping winner check.")  # Debugging

        # If it's the AI's turn, make the AI move
        if isinstance(self.players[self.current_turn], ComputerPlayer):
            print(f"Computer player {self.current_turn + 1} is making a move...")  # Debugging
            move = self.players[self.current_turn].make_move()  # Capture move details

            # If no valid move was found by the computer, end the turn
            if move is None:
                print("No valid move found by the computer.")
                self.end_turn()
            else:
                # If a valid move is found, log the move and update the game state
                start_row, start_col, end_row, end_col = move
                self.add_to_move_history(self.board.get_piece(end_row, end_col), start_row, start_col, end_row, end_col)
                self.end_turn()  # Move to the next player after the AI move

        # If it's the human player's turn, wait for input via mouse clicks
        elif isinstance(self.players[self.current_turn], HumanPlayer):
            print(f"Human player {self.current_turn + 1}'s turn.")  # Debugging
            # The game will continue waiting for input, which is handled elsewhere

        # Handle unknown player types by skipping their turn
        else:
            print(f"Unknown player type. Turn skipped.")  # Debugging

    """
    Function Name: display_error_message
    Purpose: Displays any error messages (e.g., invalid moves).
    Parameters: None
    Return Value: None
    Algorithm:
        1) If an error message exists, render it in red on the game window.
        2) Use the game's font to display the error message at a fixed position.
    Reference: None
    """

    def display_show_history_button(self):
        # Draw the rectangle for the "Show History" button
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)
        # Create a font object for rendering the button text
        font = pygame.font.SysFont('Arial', 20)
        # Render the "Show History" text in white
        text_surface = font.render("Show History", True, (255, 255, 255))
        # Center the text on the button rectangle
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)
        # Blit the button text onto the game window
        self.window.blit(text_surface, text_rect)

    """
    Function Name: display_show_history_button
    Purpose: Displays a button to show move history.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Draw a rectangle on the screen for the move history button.
        2) Render the button label "Show History" at the center of the rectangle.
    Reference: None
    """

    def display_show_history_button(self):

        # Draw a black rectangle representing the "Show History" button on the game window
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)

        # Create a font object for rendering the button text
        font = pygame.font.SysFont('Arial', 20)

        # Render the "Show History" text in white
        text_surface = font.render("Show History", True, (255, 255, 255))

        # Get the rectangle where the text will be placed, centered inside the button
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)

        # Blit the text surface onto the button's rectangle on the window
        self.window.blit(text_surface, text_rect)

    """
    Function Name: handle_click
    Purpose: Handles mouse clicks during the game to execute specific actions.
    Parameters: 
        pos (tuple): The (x, y) coordinates of the mouse click.
    Return Value: None
    Algorithm:
        1) Check if the click is on specific buttons (history, save, or help).
        2) If not, handle board interactions (selecting/moving pieces).
    Reference: Chatgpt
    """

    def handle_click(self, pos):

        # Check if the click is within the "Show History" button
        if self.show_history_button_rect.collidepoint(pos):
            self.show_move_history_popup()  # Show move history when the button is clicked

        # Check if the click is within the "Save Game" button
        elif self.save_game_button_rect.collidepoint(pos):
            self.save_game_state()  # Save the game when the button is clicked

        # Check if the click is within the "Help" button
        elif self.help_button_rect.collidepoint(pos):
            self.display_help()  # Display help when the Help button is clicked

        # Handle interactions with the game board (selecting and moving pieces)
        else:
            row, col = self.get_row_col_from_mouse(pos)
            if row is not None and col is not None:
                if self.selected_piece:
                    self.move_piece(row, col)  # Move the selected piece to the clicked location
                else:
                    self.select_piece(row, col)  # Select a piece at the clicked location

    """
    Function Name: show_move_history_popup
    Purpose: Displays the move history in a popup window.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Create a new popup window to display the move history.
        2) Render each move in the move history vertically, scrolling if necessary.
    Reference: None
    """

    def show_move_history_popup(self):
        # Set the dimensions of the popup window for move history
        popup_width, popup_height = 400, 600

        # Create a new popup window with the specified dimensions
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Move History")  # Set the title of the popup window

        running = True
        while running:
            # Handle events within the popup window (closing or exiting with escape key)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Fill the popup window with a light background color
            popup_window.fill((240, 240, 240))

            # Display each move from the move history in the popup window
            y_position = 20  # Start drawing moves from the top of the popup
            for move in self.move_history:
                move_surface = self.history_font.render(move, True, (0, 0, 0))  # Render each move as text
                popup_window.blit(move_surface, (20, y_position))  # Blit the move onto the popup window
                y_position += move_surface.get_height() + 5  # Move down to the next line

            # Update the popup window display
            pygame.display.flip()

        # Restore the main game window after the popup is closed
        self.window = pygame.display.set_mode((800, 800))

    """
    Function Name: check_winner
    Purpose: Checks if a player has won by forming a connected group of pieces.
    Parameters: None
    Return Value: None
    Algorithm:
        1) For each player color, check if the board contains a connected group.
        2) If a connected group is found, declare the player as the winner and display the result.
    Reference: None
    """

    def check_winner(self):
        # Only check for a winner if one hasn't already been displayed
        if not self.winner_displayed:
            print("Checking for winner...")  # Debugging

            # Get the list of colors to check for connected groups
            if self.num_players == 2:
                colors = [self.player_color, self.computer_color]
            else:
                colors = list(self.player_colors.values())  # Extract player colors in 4-player mode

            # Loop through each color to check for a winning connected group
            for color in colors:
                if self.board.check_connected_group(color):
                    print(f"Winner found: {self.get_color_name(color)}")  # Debugging

                    # Display the winner and stop further checks
                    self.display_winner(color)
                    self.winner_displayed = True  # Stop further winner checks
                    print(f"Winner flag set to {self.winner_displayed} after finding winner")  # Debugging
                    break  # Exit loop once a winner is found
            else:
                print("No winner found yet.")  # Debugging

    """
    Function Name: display_winner
    Purpose: Displays the winner in a popup window and shows scores and rounds won.
    Parameters: 
        color (tuple): The RGB color of the winning player.
    Return Value: None
    Algorithm:
        1) Create a popup window to show the winner's information.
        2) Display scores and rounds won by all players.
    Reference: None
    """

    def display_winner(self, color):

        print(f"Displaying winner: {self.get_color_name(color)}")  # Debugging

        # Get the player number corresponding to the winning color
        player_number = self.get_player_number(color)

        # Update the player's score and rounds won
        self.update_score(player_number, color)

        # Create a popup window to display the winner's information
        popup_width, popup_height = 400, 300  # Popup window dimensions
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Game Over")  # Set the popup window's title

        # Use a large font to display the winner's name
        font = pygame.font.SysFont('Arial', 30)
        color_name = self.get_color_name(color)
        text_surface = font.render(f"Player {player_number} ({color_name}) Wins!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_width // 2, 50))  # Position the text at the top of the popup

        # Use a smaller font for displaying scores and rounds
        info_font = pygame.font.SysFont('Arial', 20)

        # Prepare text for displaying player scores and rounds won
        scores_text = [f"Player {i + 1} - Rounds Won: {self.player_wins[i]}, Score: {self.player_scores[i]}"
                       for i in range(self.num_players)]
        scores_surfaces = [info_font.render(score_text, True, (0, 0, 0)) for score_text in scores_text]

        running = True
        while running:
            # Handle events within the popup window (close window on quit or Enter key)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False  # Close the popup when Enter is pressed

            # Fill the popup window with a light background color
            popup_window.fill((240, 240, 240))

            # Display the winner's text at the top of the popup
            popup_window.blit(text_surface, text_rect)

            # Display the scores and rounds won for all players
            y_offset = 100  # Start displaying scores below the winner's text
            for surface in scores_surfaces:
                popup_window.blit(surface, (20, y_offset))  # Display each score on a new line
                y_offset += 30  # Move down for the next line of text

            # Update the popup display
            pygame.display.flip()

        # After displaying the winner, prompt the user to replay or quit
        self.ask_replay()
    """
    Function Name: get_player_number
    Purpose: Returns the player number corresponding to the given color.
    Parameters:
        color (tuple): The RGB color of the player.
    Return Value: 
        int: The player number (1-based index).
        If the color is not found, returns "Unknown".
    Algorithm:
        1) For 2-player mode, return 1 if the color matches player_color and 2 if it matches computer_color.
        2) For 4-player mode, loop through the player_colors dictionary to find the matching color.
    Reference: None
    """

    def get_player_number(self, color):
        if self.num_players == 2:
            # Handle 2-player mode
            if color == self.player_color:
                return 1  # Player 1
            elif color == self.computer_color:
                return 2  # Player 2 (Computer)
        else:
            # Handle 4-player mode
            for player_num, player_color in self.player_colors.items():
                if player_color == color:
                    return player_num
        return "Unknown"

    """
    Function Name: update_score
    Purpose: Updates the score for the player who won the round.
    Parameters:
        player_number (int): The number of the winning player.
        color (tuple): The RGB color of the winning player.
    Return Value: None
    Algorithm:
        1) Count the winner's and opponent's remaining pieces on the board.
        2) Calculate the score difference and update the player's score.
        3) Increment the rounds won for the winning player.
        4) Set the previous_winner_color to the current winner's color.
    Reference: None
    """

    def update_score(self, player_number, color):
        # Count the number of pieces remaining for the winning player
        winner_pieces = len([piece for piece in self.board.pieces if piece.color == color])

        # Determine the opponent's color
        opponent_color = self.computer_color if color == self.player_color else self.player_color
        # Count the number of pieces remaining for the opponent
        opponent_pieces = len([piece for piece in self.board.pieces if piece.color == opponent_color])

        # Calculate the score difference based on the number of remaining pieces
        score_difference = winner_pieces - opponent_pieces
        # Update the score for the winning player
        self.player_scores[player_number - 1] += score_difference

        # Increment the round wins for the winning player
        self.player_wins[player_number - 1] += 1

        # Store the color of the previous winner for future rounds
        self.previous_winner_color = color

        # Log the updated scores and rounds won for debugging purposes
        print(f"Updated Score for Player {player_number}: {self.player_scores[player_number - 1]}")
        print(f"Rounds Won by Player {player_number}: {self.player_wins[player_number - 1]}")

    """
    Function Name: ask_replay
    Purpose: Prompts the player to replay the game or quit.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Create a popup window with Yes and No buttons.
        2) If Yes is clicked, reset the game.
        3) If No is clicked, exit the game.
    Reference: None
    """

    def ask_replay(self):
        # Log that the replay prompt is being shown
        print("Asking the user if they want to replay...")  # Debugging

        # Set up the popup window dimensions and title
        popup_width, popup_height = 400, 200
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Play Again?")

        # Create the font and render the prompt asking to replay
        font = pygame.font.SysFont('Arial', 24)
        prompt_surface = font.render("Play Again?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(popup_width // 2, popup_height // 2 - 30))

        # Set up Yes and No buttons with specific dimensions and positions
        yes_button_rect = pygame.Rect(popup_width // 2 - 60, popup_height // 2 + 20, 50, 30)
        no_button_rect = pygame.Rect(popup_width // 2 + 10, popup_height // 2 + 20, 50, 30)

        # Display loop for handling the player's choice to replay or exit
        running = True
        while running:
            for event in pygame.event.get():
                # Exit the game if the user closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse clicks on the Yes and No buttons
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button_rect.collidepoint(event.pos):
                        print("User chose to replay.")  # Debugging
                        self.reset_game()  # Reset the game state
                        running = False  # Exit the loop
                    elif no_button_rect.collidepoint(event.pos):
                        print("User chose not to replay. Exiting...")  # Debugging
                        pygame.quit()
                        exit()

            # Fill the popup window with a light background color
            popup_window.fill((240, 240, 240))

            # Display the replay prompt in the center of the popup window
            popup_window.blit(prompt_surface, prompt_rect)

            # Draw the Yes and No buttons with green and red colors, respectively
            pygame.draw.rect(popup_window, (0, 255, 0), yes_button_rect)  # Green for Yes
            pygame.draw.rect(popup_window, (255, 0, 0), no_button_rect)  # Red for No

            # Render the text for the Yes and No buttons and display it on the buttons
            yes_text = font.render("Yes", True, (0, 0, 0))
            no_text = font.render("No", True, (0, 0, 0))

            popup_window.blit(yes_text, yes_button_rect.move(5, 0))
            popup_window.blit(no_text, no_button_rect.move(10, 0))

            # Update the popup display
            pygame.display.flip()

        # Restore the main game window after the popup is closed
        self.window = pygame.display.set_mode((800, 800))

    """
    Function Name: get_row_col_from_mouse
    Purpose: Returns the row and column based on the mouse click position.
    Parameters:
        pos (tuple): The (x, y) position of the mouse click.
    Return Value:
        tuple: The row and column corresponding to the mouse position or (None, None) if the click is outside the board.
    Algorithm:
        1) Extract the x and y coordinates from the mouse click position.
        2) Subtract the board's offset to account for positioning.
        3) Divide by the grid size to compute the row and column.
        4) If the calculated row and column are valid, return them. Otherwise, return None, None.
    Reference: Chatgpt
    """

    def get_row_col_from_mouse(self, pos):
        # Extract x and y coordinates from the mouse position
        x, y = pos

        # Get the offset and grid size of the board
        board_offset = self.board.offset
        grid_size = self.board.grid_size

        # Check if the click is within the board area
        if x < board_offset or y < board_offset:
            return None, None

        # Calculate the row and column based on the mouse position
        row = (y - board_offset) // grid_size
        col = (x - board_offset) // grid_size

        # Ensure the calculated row and column are within the board limits
        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            return row, col
        return None, None

    """
    Function Name: select_piece
    Purpose: Handles selecting a piece on the board.
    Parameters:
        row (int): The row of the piece to be selected.
        col (int): The column of the piece to be selected.
    Return Value: None
    Algorithm:
        1) Get the piece at the specified row and column.
        2) If the piece exists and it is the correct player's turn, select the piece.
        3) Clear any error messages if the selection is successful.
    Reference: None
    """

    def select_piece(self, row, col):
        # Get the piece at the specified row and column
        piece = self.board.get_piece(row, col)

        # Check if the piece exists and if it's the correct player's turn
        if piece and self.is_correct_turn(piece):
            # Debugging statement for selected piece
            print(f"Selected piece at {row}, {col} for {self.get_color_name(piece.color)}.")

            # Set the selected piece and clear any error messages
            self.selected_piece = piece
            self.error_message = ""  # Clear error message when a piece is successfully selected

    """
    Function Name: move_piece
    Purpose: Handles moving a selected piece on the board.
    Parameters:
        row (int): The target row for the piece to move to.
        col (int): The target column for the piece to move to.
    Return Value: None
    Algorithm:
        1) If a piece is selected, validate the move to the target position.
        2) If the move is valid, update the board and add the move to history.
        3) End the player's turn after a successful move.
        4) If the move is invalid, show an error message and deselect the piece.
    Reference: None
    """

    def move_piece(self, row, col):
        # Check if a piece is selected for movement
        if self.selected_piece:
            # Get the starting row and column of the selected piece
            start_row = self.selected_piece.row
            start_col = self.selected_piece.col

            # Validate the move to the target row and column
            is_valid, message = self.board.is_valid_move(self.selected_piece, row, col)

            # If the move is valid, proceed with moving the piece
            if is_valid:
                # Debugging statement for moving the piece
                print(f"Moving piece from {start_row}, {start_col} to {row}, {col}.")

                # Add the move to the move history
                self.add_to_move_history(self.selected_piece, start_row, start_col, row, col)

                # Update the board by moving the piece to the new location
                self.board.move_piece(self.selected_piece, row, col)

                # End the player's turn after a successful move
                self.end_turn()

                # Clear any error messages
                self.error_message = ""
            else:
                # Debugging statement for invalid move
                print(f"Invalid move attempted: {message}")

                # Display the error message and deselect the piece
                self.error_message = message
                self.selected_piece = None

    """
    Function Name: end_turn
    Purpose: Ends the current player's turn and switches to the next player.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Set the selected_piece to None.
        2) Increment the current_turn variable by 1 and mod by the number of players to loop turns.
        3) Print the current turn for debugging purposes.
    Reference: None
    """

    def end_turn(self):
        # Deselect the current piece after the turn ends
        self.selected_piece = None

        # Increment the current turn to the next player, wrapping around if necessary
        self.current_turn = (self.current_turn + 1) % self.num_players

        # Debugging statement to show the next player's turn
        print(f"Turn ended. Next player's turn: {self.current_turn}")
    """
    Function Name: is_correct_turn
    Purpose: Checks if it's the correct player's turn to move the selected piece.
    Parameters: 
        piece (Piece): The piece that the player is trying to move.
    Return Value: 
        bool: True if it's the correct turn for the piece's color, False otherwise.
    Algorithm:
        1) For 2-player mode, check if the current turn matches the piece's color (player or computer).
        2) For 4-player mode, find the color of the current player and match it with the piece's color.
    Reference: None
    """

    def is_correct_turn(self, piece):
        # Check if it's a 2-player game
        if self.num_players == 2:
            # If it's the player's turn (turn 0), check if the piece matches the player's color
            if self.current_turn == 0:
                return piece.color == self.player_color
            # If it's the computer's turn (turn 1), check if the piece matches the computer's color
            else:
                return piece.color == self.computer_color
        else:
            # For 4-player mode, find the current player's color based on the player number
            current_color = \
                [(player, color) for player, color in self.player_colors.items() if player == self.current_turn + 1][0][
                    1]

            # Return True if the piece's color matches the current player's color
            return piece.color == current_color

    """
    Function Name: add_to_move_history
    Purpose: Adds the current move to the move history with a descriptive message.
    Parameters:
        piece (Piece): The piece being moved.
        start_row (int): The row where the piece started.
        start_col (int): The column where the piece started.
        end_row (int): The row where the piece ended.
        end_col (int): The column where the piece ended.
    Return Value: None
    Algorithm:
        1) Convert the start and end positions to notation.
        2) Get the player number and color for the piece.
        3) Append the move to the move history in a descriptive format.
    Reference: None
    """

    def add_to_move_history(self, piece, start_row, start_col, end_row, end_col):
        # Convert the start and end positions to chess-like notation
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)

        # Get the player number and color name for the piece being moved
        player_number = self.get_player_number(piece.color)
        color_name = self.get_color_name(piece.color)

        # Create a descriptive move message and append it to the move history
        move = f"Player {player_number} ({color_name}) moved {start_notation} to {end_notation}"
        self.move_history.append(move)

        # Debugging statement to confirm the move was added to history
        print(f"Move added to history: {move}")

    """
    Function Name: get_color_name
    Purpose: Converts an RGB color tuple to a string representing the color name.
    Parameters: 
        color (tuple): The RGB tuple representing the color.
    Return Value: 
        str: The name of the color (Black, White, Red, Green, or Unknown).
    Algorithm:
        1) Match the RGB color tuple to a string representing the color name.
    Reference: None
    """

    def get_color_name(self, color):
        # Return the name corresponding to the given RGB color
        if color == (0, 0, 0):
            return "Black"
        elif color == (255, 255, 255):
            return "White"
        elif color == (255, 0, 0):
            return "Red"
        elif color == (0, 255, 0):
            return "Green"
        else:
            return "Unknown"

    """
    Function Name: display_save_game_button
    Purpose: Displays the 'Save Game' button on the game window.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Draw a black rectangle representing the button.
        2) Render the text 'Save Game' inside the button.
        3) Blit the button text onto the game window.
    Reference: None
    """

    def display_save_game_button(self):
        # Draw the button rectangle on the window for the "Save Game" button
        pygame.draw.rect(self.window, (0, 0, 0), self.save_game_button_rect)

        # Create the font and render the text for the button
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Save Game", True, (255, 255, 255))  # White text for the button

        # Position the text at the center of the button
        text_rect = text_surface.get_rect(center=self.save_game_button_rect.center)

        # Display the button text on the game window
        self.window.blit(text_surface, text_rect)
    """
    Function Name: save_game_state
    Purpose: Saves the current state of the game to a file.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Open the save file in write mode.
        2) Write the current board state to the file.
        3) Write the player information (if 2-player mode).
        4) Write the move history.
        5) Write the current turn information.
    Reference: None
    """

    def save_game_state(self):
        # Specify the file path for saving the game state
        save_file_path = "game_state.txt"

        try:
            # Open the file in write mode to save the game state
            with open(save_file_path, 'w') as save_file:
                # Write the current board state to the file
                save_file.write("Board:\n")
                for row in range(self.board.rows):
                    for col in range(self.board.cols):
                        piece = self.board.get_piece(row, col)
                        if piece:
                            # Get the color symbol for the piece (e.g., 'B' for Black)
                            piece_symbol = self.get_color_symbol(piece.color)
                        else:
                            # Use '.' for empty spaces on the board
                            piece_symbol = '.'
                        save_file.write(piece_symbol + ' ')
                    save_file.write('\n')

                # Write player information if in 2-player mode
                if self.num_players == 2:
                    save_file.write("\nPlayers:\n")
                    save_file.write("Player 1 Color: " + self.get_color_name(self.player_color) + "\n")
                    save_file.write("Player 2 Color: " + self.get_color_name(self.computer_color) + "\n")

                # Write the move history to the file
                save_file.write("\nMove History:\n")
                for move in self.move_history:
                    save_file.write(move + "\n")

                # Write the current turn information (which player is next)
                save_file.write("\nCurrent Turn: Player " + str(self.current_turn + 1) + "\n")

            # Confirm in the console that the game state was saved successfully
            print("Game state saved successfully.")

        # Handle exceptions and print an error message if saving fails
        except Exception as e:
            print(f"Error saving game state: {e}")

    """
    Function Name: get_color_symbol
    Purpose: Returns a single-character symbol representing the piece color.
    Parameters: 
        color (tuple): RGB color tuple representing the piece's color.
    Return Value: 
        str: A single-character string representing the color ('B' for Black, 'W' for White, etc.).
    Algorithm:
        1) Check the color tuple and return the corresponding symbol.
    Reference: None
    """

    def get_color_symbol(self, color):
        # Return the appropriate symbol for the given piece color
        if color == (0, 0, 0):
            return 'B'  # Black piece
        elif color == (255, 255, 255):
            return 'W'  # White piece
        elif color == (255, 0, 0):
            return 'R'  # Red piece
        elif color == (0, 255, 0):
            return 'G'  # Green piece
        else:
            return '.'  # Unknown color or empty space

    """
    Function Name: load_game_state
    Purpose: Loads a saved game state from a file.
    Parameters: 
        case_number (int): The case number representing the saved game state file.
    Return Value: None
    Algorithm:
        1) Check if the file exists.
        2) Read the file and extract the board state.
        3) Load player information and determine turn.
        4) Recreate the players based on the saved data.
    Reference: None
    """

    def load_game_state(self, case_number):
        # Construct the file path for the saved game case
        file_path = f"game_case_{case_number}.txt"

        # Check if the file exists before attempting to load
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found.")
            return

        try:
            # Open the saved game file for reading
            with open(file_path, 'r') as load_file:
                lines = load_file.readlines()
                print(f"Loaded lines: {lines}")  # Debugging statement

                # Initialize the board and clear any existing pieces
                self.board = Board(self.board_size, initialize=False)
                self.board.clear_board()  # This now works with the corrected method
                print("Initializing board from loaded state...")

                # Load the board state from the file
                board_section = lines[1:self.board_size + 1]
                for row, line in enumerate(board_section):
                    pieces = line.strip().split()
                    for col, piece_symbol in enumerate(pieces):
                        piece_symbol = piece_symbol.upper()  # Convert to uppercase
                        if piece_symbol == 'B':
                            color_rgb = (0, 0, 0)  # Black piece RGB
                            self.board.set_piece(row, col, color_rgb)
                        elif piece_symbol == 'W':
                            color_rgb = (255, 255, 255)  # White piece RGB
                            self.board.set_piece(row, col, color_rgb)

                # Extract next player and color information from the file
                next_player_line = lines[-2].strip().split(": ")[1]  # Should be 'Human' or 'Computer'
                next_color_line = lines[-1].strip().split(": ")[1]  # Should be 'White' or 'Black'

                # Determine the player and computer color based on the file data
                if next_player_line == "Computer":
                    if next_color_line == "Black":
                        self.computer_color = (0, 0, 0)
                        self.player_color = (255, 255, 255)
                    else:  # White
                        self.computer_color = (255, 255, 255)
                        self.player_color = (0, 0, 0)
                    self.current_turn = 1  # Computer's turn
                else:  # Human
                    if next_color_line == "Black":
                        self.player_color = (0, 0, 0)
                        self.computer_color = (255, 255, 255)
                    else:  # White
                        self.player_color = (255, 255, 255)
                        self.computer_color = (0, 0, 0)
                    self.current_turn = 0  # Human's turn

                print(f"Player color set to: {self.get_color_name(self.player_color)}")
                print(f"Computer color set to: {self.get_color_name(self.computer_color)}")
                print(f"Current turn set to: {self.current_turn}")

                # Create the players after setting the player colors
                self.players = self.create_players()

                print("Game state loaded successfully.")

        # Handle errors that occur during loading
        except Exception as e:
            print(f"Error loading game state: {e}")

    """
    Function Name: display_help_button
    Purpose: Displays the 'Help' button on the game screen.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Draw a rectangle for the button on the screen.
        2) Render the text "Help" on top of the button.
        3) Display the button on the window.
    Reference: None
    """

    def display_help_button(self):
        # Draw the help button rectangle on the window
        pygame.draw.rect(self.window, (0, 0, 0), self.help_button_rect)

        # Create the font and render the "Help" text for the button
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Help", True, (255, 255, 255))  # White text for the button

        # Position the text at the center of the button
        text_rect = text_surface.get_rect(center=self.help_button_rect.center)

        # Display the button text on the game window
        self.window.blit(text_surface, text_rect)
    """
    Function Name: display_help
    Purpose: Displays all possible valid moves for the human player in a popup window.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Generate all possible valid and capture moves for the human player.
        2) Create a popup window to display the help information.
        3) Render the possible moves and capture moves within the popup window.
        4) Close the popup when the user quits or presses ESCAPE.
    Reference: None
    """

    def display_help(self):
        # Generate all valid and capture moves for the human player
        possible_moves, capture_moves = self.generate_human_player_moves()

        # Create a popup window to display the help information
        popup_width, popup_height = 400, 600
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Help - Possible Moves")

        # Set the font for rendering text in the popup
        font = pygame.font.SysFont('Arial', 20)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # Fill the popup window with a light background color
            popup_window.fill((240, 240, 240))

            y_position = 20

            # Display capture moves if available
            if capture_moves:
                capture_title = font.render("Capture Moves:", True, (0, 0, 0))
                popup_window.blit(capture_title, (20, y_position))
                y_position += 30
                for move in capture_moves:
                    move_surface = font.render(move, True, (0, 0, 0))
                    popup_window.blit(move_surface, (20, y_position))
                    y_position += move_surface.get_height() + 5

            # Display non-capture moves if available
            if possible_moves:
                non_capture_title = font.render("Possible Moves:", True, (0, 0, 0))
                popup_window.blit(non_capture_title, (20, y_position))
                y_position += 30
                for move in possible_moves:
                    move_surface = font.render(move, True, (0, 0, 0))
                    popup_window.blit(move_surface, (20, y_position))
                    y_position += move_surface.get_height() + 5

            # Update the display with the rendered text
            pygame.display.flip()

        # Restore the main game window after the popup is closed
        self.window = pygame.display.set_mode((800, 800))

    """
    Function Name: generate_human_player_moves
    Purpose: Generates all possible valid moves and capture moves for the human player.
    Parameters: None
    Return Value: 
        tuple: A tuple containing two lists, one for valid moves and one for capture moves.
    Algorithm:
        1) Determine the current player's color based on the current turn.
        2) Iterate through all pieces on the board.
        3) For each piece of the current player's color, generate possible and capture moves.
        4) Return the lists of possible moves and capture moves.
    Reference: None
    """

    def generate_human_player_moves(self):
        # Initialize lists for possible moves and capture moves
        possible_moves = []
        capture_moves = []
        # Get the current player's color based on whose turn it is
        color = self.player_color if self.current_turn == 0 else self.computer_color

        # Iterate through all pieces on the board
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    # Generate valid and capture moves for this piece
                    moves, captures = self.generate_moves_for_piece(row, col)
                    possible_moves.extend(moves)
                    capture_moves.extend(captures)

        # Return the lists of possible and capture moves
        return possible_moves, capture_moves

    """
    Function Name: generate_moves_for_piece
    Purpose: Generates valid moves for a specific piece on the board.
    Parameters: 
        start_row (int): The row of the piece being moved.
        start_col (int): The column of the piece being moved.
    Return Value: 
        tuple: Two lists, one for valid moves and one for capture moves.
    Algorithm:
        1) Get the piece at the starting position.
        2) Calculate the number of moves required in horizontal, vertical, and diagonal directions.
        3) For each direction, check if the move is valid and add it to the move or capture list.
    Reference: None
    """

    def generate_moves_for_piece(self, start_row, start_col):
        # Initialize lists for valid moves and capture moves
        moves = []
        captures = []
        # Get the piece located at the given row and column
        piece = self.board.get_piece(start_row, start_col)

        # Calculate required moves in horizontal, vertical, and diagonal directions
        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)

        # Horizontal moves
        for offset in range(1, horizontal_moves_required + 1):
            # Check right and left moves for validity
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col + offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col - offset, moves, captures)

        # Vertical moves
        for offset in range(1, vertical_moves_required + 1):
            # Check down and up moves for validity
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col, moves, captures)

        # Diagonal moves
        for offset in range(1, diagonal_moves_required + 1):
            # Check all diagonal directions for validity
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col + offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col - offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col - offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col + offset, moves, captures)

        # Return the lists of valid and capture moves
        return moves, captures

    """
    Function Name: add_human_move_if_valid
    Purpose: Adds a move to the list if it is valid.
    Parameters: 
        start_row (int): The starting row of the piece.
        start_col (int): The starting column of the piece.
        end_row (int): The row where the piece is moved to.
        end_col (int): The column where the piece is moved to.
        moves (list): The list of valid moves.
        captures (list): The list of capture moves.
    Return Value: None
    Algorithm:
        1) Check if the end row and column are within bounds of the board.
        2) Validate the move and check for captures.
        3) Add the move to the appropriate list based on validation results.
    Reference: None
    """

    def add_human_move_if_valid(self, start_row, start_col, end_row, end_col, moves, captures):
        # Ensure the move is within the bounds of the board
        if 0 <= end_row < self.board.rows and 0 <= end_col < self.board.cols:
            # Validate the move and check for any captures
            is_valid, captures_list = self.validate_move(start_row, start_col, end_row, end_col)
            # Convert the start and end positions to chess-like notation
            start_notation = self.board.get_position_notation(start_row, start_col)
            end_notation = self.board.get_position_notation(end_row, end_col)
            # Create a move string describing the move
            move = f"{start_notation} to {end_notation}"
            if is_valid:
                if captures_list:
                    captures.append(move)  # Add to capture moves if valid
                else:
                    moves.append(move)  # Add to valid moves if no captures

    """
    Function Name: validate_move
    Purpose: Validates whether a move is allowed and checks for captures.
    Parameters: 
        start_row (int): The starting row of the piece.
        start_col (int): The starting column of the piece.
        end_row (int): The row where the piece is moved to.
        end_col (int): The column where the piece is moved to.
    Return Value: 
        tuple: A boolean indicating if the move is valid, and a list of captured pieces.
    Algorithm:
        1) Check if the piece at the start belongs to the human player.
        2) Use the board's move validation logic to determine if the move is valid.
        3) Check if the move results in capturing an opponent's piece and return the results.
    Reference: None
    """

    def validate_move(self, start_row, start_col, end_row, end_col):
        # Initialize an empty list for captured pieces
        captures = []
        # Get the piece at the starting position
        piece = self.board.get_piece(start_row, start_col)
        # Ensure the piece belongs to the human player before validating the move
        if not piece or piece.color != self.player_color:
            return False, captures

        # Use the board's validation logic to check the move
        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            # Check if an opponent's piece is captured
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.player_color:
                captures.append((end_row, end_col))  # Add the captured piece to the list
            return True, captures  # Return valid status and captures
        return False, captures  # Return invalid status

    """
    Function Name: display_current_player
    Purpose: Displays the current player's turn on the game screen.
    Parameters: 
        self: The instance of the Game class, which holds game state and player information.
    Return Value: 
        None
    Algorithm:
        1) Determine if it's 2-player or 4-player mode.
        2) In 2-player mode, identify if it's the human or computer's turn.
        3) In 4-player mode, find the current player based on the player number.
        4) Get the corresponding player color and construct a message showing whose turn it is.
        5) Render the message and display it at the top of the game window.
        6) If it's the computer's turn, add a brief pause before the computer makes its move.
    Reference: None
    """

    def display_current_player(self):
        # For 2-player mode, determine if it's the human or computer's turn
        if self.num_players == 2:
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            color = self.player_color if self.current_turn == 0 else self.computer_color  # Get current player's color
            color_name = self.get_color_name(color)  # Convert color to name for display
        else:
            # For 4-player mode, get the player number and type (Human/Computer)
            player_number = self.current_turn + 1
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            color = self.player_colors[player_number]  # Get the current player's color
            color_name = self.get_color_name(color)  # Convert color to name for display

        # Construct a message to show whose turn it is
        turn_text = f"{player_type} (Player {self.current_turn + 1}, {color_name})'s turn"

        # Set up the font and render the text message in black
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(turn_text, True, (0, 0, 0))  # Black text
        # Display the message at the top of the game window
        self.window.blit(text_surface, (300, 10))
        pygame.display.update()  # Update the display to show the current player's turn

        # Add a brief pause if it's the computer's turn
        if player_type == "Computer":
            pygame.time.wait(500)

    def display_error_message(self):
        """Displays any error messages (e.g., invalid moves)."""
        if self.error_message:
            # Set up the font for displaying the error message
            font = pygame.font.SysFont('Arial', 24)
            # Render the error message in red
            text_surface = font.render(self.error_message, True, (255, 0, 0))
            # Display the error message in the top left corner of the game window
            self.window.blit(text_surface, (10, 10))

