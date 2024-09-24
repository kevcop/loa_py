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
        self.window = window
        self.num_players = num_players
        self.players_type = players_type
        self.player_order = player_order if player_order is not None else []
        self.player_colors = player_colors if player_colors is not None else {}
        self.board_size = board_size
        self.player_color = player_color  # For 2-player mode
        self.computer_color = computer_color  # For 2-player mode
        self.selected_piece = None
        self.error_message = ""  # To store error messages
        self.move_history = []  # List to store move history
        self.history_font = pygame.font.SysFont('Arial', 20)
        self.history_box_height = 150  # Height of the move history box
        self.history_offset = 10  # Padding within the history box
        self.show_history_button_rect = pygame.Rect(650, 20, 140, 50)  # Button to show move history
        self.save_game_button_rect = pygame.Rect(650, 80, 140, 50)  # Save Game button position and size
        self.help_button_rect = pygame.Rect(650, 140, 140, 50)         # Help button
        self.winner_displayed = False  # Track if the winner has been displayed
        self.players = []  # List to store the players (Human or AI)
        self.current_turn = 0  # Initialize current_turn to 0
        self.player_wins = {i: 0 for i in range(self.num_players)}  # Initialize rounds won for each player
        self.player_scores = {i: 0 for i in range(self.num_players)}  # Initialize scores for each player
        self.previous_winner_color = None  # Track the color of the previous round's winner

        print(f"Initializing game with {num_players} players.")  # Debugging player count

        if case:
            # Load the game state from the specified case file
            self.load_game_state(case)
        else:
            # Initialize the game normally
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
        print("Resetting the game for a new round...")  # Debugging

        # Ensure the winner flag is properly reset
        self.winner_displayed = False
        print(f"Winner flag reset: {self.winner_displayed}")  # Debugging the reset of the winner flag

        # Reinitialize the board and verify it has no pieces
        self.board = Board(self.board_size)
        print("New board initialized with size", self.board_size)  # Debugging board reset
        print(f"Board state after reset: {self.board.pieces}")  # Debugging to check if pieces are cleared

        self.selected_piece = None
        self.error_message = ""
        self.move_history = []
        self.players = self.create_players()  # Recreate players for the new game
        print(f"Players created: {self.players}")  # Debugging

        # Check player count and player list integrity
        print(f"Number of players: {len(self.players)}")  # Debugging player count
        if len(self.players) != self.num_players:
            print(f"Error: Expected {self.num_players} players but got {len(self.players)}")

        # Reset move history and error messages
        print("Move history cleared, and error messages reset.")

        # Ensure proper first turn setup for 2-player or 4-player mode
        if self.num_players == 2:
            # Swap colors only if the previous winner was the player with the white pieces
            if self.previous_winner_color == (255, 255, 255) and self.player_wins[0] != self.player_wins[1]:
                # Swap colors: the player (who was white) now plays with black
                self.player_color, self.computer_color = self.computer_color, self.player_color
                print(f"Swapping colors. Player color: {self.get_color_name(self.player_color)}, "
                      f"Computer color: {self.get_color_name(self.computer_color)}")

            # Set the current turn based on who has the black pieces
            if self.player_color == (0, 0, 0):  # Black
                self.current_turn = 0  # Player moves first
                print("Player (Black) moves first.")
            else:
                self.current_turn = 1  # Computer moves first
                print("Computer (Black) moves first.")
        else:
            # For 4-player mode, reset player turns starting with black
            black_player = [player for player, color in self.player_colors.items() if color == (0, 0, 0)][0]
            self.current_turn = black_player - 1  # Set the current turn to the player assigned to Black
            print(f"Player {black_player} (Black) moves first.")  # Debugging

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
        players = []
        print("Creating players...")  # Debugging

        if self.num_players == 2:
            colors = [self.player_color, self.computer_color]
            print(f"2-player game with colors: {colors}")  # Debugging
            for i in range(self.num_players):  # 0-based index for 2-player
                if self.players_type[i] == "Computer":
                    print(f"Player {i + 1} is a computer.")  # Debugging
                    players.append(ComputerPlayer(self.board, colors[i]))  # AI player
                else:
                    print(f"Player {i + 1} is a human.")  # Debugging
                    players.append(HumanPlayer())  # Use HumanPlayer class
        else:
            # In 4-player mode, use player_colors (which is a dictionary with keys 1-4)
            for i in range(1, self.num_players + 1):  # 1-based index for 4-player
                if self.players_type[i - 1] == "Computer":
                    print(f"Player {i} is a computer. Color: {self.player_colors[i]}")  # Debugging
                    players.append(ComputerPlayer(self.board, self.player_colors[i]))  # AI player
                else:
                    print(f"Player {i} is a human. Color: {self.player_colors[i]}")  # Debugging
                    players.append(HumanPlayer())  # Use HumanPlayer class

        print(f"Players created: {players}")  # Debugging
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
    Reference: None
    """
    def update(self):
        print("Game update running...")  # Debugging
        print(f"Winner flag before update: {self.winner_displayed}")  # Debugging
        print(f"Current turn: {self.current_turn}")  # Debugging
        print(f"Current player: {type(self.players[self.current_turn])}")  # Debugging

        self.winner_displayed = False
        self.window.fill((255, 255, 255))  # Fill the screen with white
        self.board.draw(self.window, self.selected_piece)  # Draw the board and pieces
        self.display_error_message()
        self.display_show_history_button()
        self.display_save_game_button()  # Display the save game button
        self.display_help_button()  # Display the Help button
        self.display_current_player()

        # Check for a winner
        if not self.winner_displayed:
            print("Checking for a winner...")  # Debugging
            self.check_winner()
        else:
            print("Winner has already been displayed, skipping winner check.")  # Debugging

        # If it's an AI's turn, make the move
        if isinstance(self.players[self.current_turn], ComputerPlayer):
            print(f"Computer player {self.current_turn + 1} is making a move...")  # Debugging
            move = self.players[self.current_turn].make_move()  # Capture move details

            if move is None:
                print("No valid move found by the computer.")
                self.end_turn()
            else:
                start_row, start_col, end_row, end_col = move
                self.add_to_move_history(self.board.get_piece(end_row, end_col), start_row, start_col, end_row, end_col)
                self.end_turn()  # Move to the next player after the AI move

        elif isinstance(self.players[self.current_turn], HumanPlayer):
            # For human player, we expect interaction via mouse clicks handled elsewhere
            print(f"Human player {self.current_turn + 1}'s turn.")  # Debugging
            # The update loop will continue waiting for the human player's input to make a move
            # This is handled through the `handle_click` method when the user interacts with the board
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

    def display_error_message(self):
        if self.error_message:
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.error_message, True, (255, 0, 0))
            self.window.blit(text_surface, (10, 10))

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
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Show History", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)
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
    Reference: None
    """

    def handle_click(self, pos):
        if self.show_history_button_rect.collidepoint(pos):
            self.show_move_history_popup()  # Show move history when the button is clicked
        elif self.save_game_button_rect.collidepoint(pos):
            self.save_game_state()  # Save the game when the button is clicked
        elif self.help_button_rect.collidepoint(pos):
            self.display_help()  # Display help for the human player when the Help button is clicked
        else:
            # Handle selecting and moving pieces as usual
            row, col = self.get_row_col_from_mouse(pos)
            if row is not None and col is not None:
                if self.selected_piece:
                    self.move_piece(row, col)
                else:
                    self.select_piece(row, col)

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
        popup_width, popup_height = 400, 600
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Move History")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            popup_window.fill((240, 240, 240))

            y_position = 20
            for move in self.move_history:
                move_surface = self.history_font.render(move, True, (0, 0, 0))
                popup_window.blit(move_surface, (20, y_position))
                y_position += move_surface.get_height() + 5

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
        if not self.winner_displayed:
            print("Checking for winner...")  # Debugging
            if self.num_players == 2:
                colors = [self.player_color, self.computer_color]
            else:
                colors = list(self.player_colors.values())  # Correct way to extract player colors

            for color in colors:
                if self.board.check_connected_group(color):
                    print(f"Winner found: {self.get_color_name(color)}")  # Debugging
                    self.display_winner(color)
                    self.winner_displayed = True  # Ensure we stop checking once the winner is displayed
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
        player_number = self.get_player_number(color)  # Get the player number

        # Update the player's score and rounds won
        self.update_score(player_number, color)

        popup_width, popup_height = 400, 300  # Increase the height to fit additional info
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Game Over")

        font = pygame.font.SysFont('Arial', 30)
        color_name = self.get_color_name(color)
        text_surface = font.render(f"Player {player_number} ({color_name}) Wins!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_width // 2, 50))

        # Create smaller font for scores and rounds
        info_font = pygame.font.SysFont('Arial', 20)

        # Prepare text surfaces for player scores and rounds won
        scores_text = [f"Player {i + 1} - Rounds Won: {self.player_wins[i]}, Score: {self.player_scores[i]}"
                       for i in range(self.num_players)]
        scores_surfaces = [info_font.render(score_text, True, (0, 0, 0)) for score_text in scores_text]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False  # Close the popup when Enter is pressed

            popup_window.fill((240, 240, 240))
            popup_window.blit(text_surface, text_rect)

            # Display scores and rounds
            y_offset = 100  # Start displaying below the winner text
            for surface in scores_surfaces:
                popup_window.blit(surface, (20, y_offset))
                y_offset += 30  # Move down for the next line of text

            pygame.display.flip()

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
        winner_pieces = len([piece for piece in self.board.pieces if piece.color == color])
        opponent_color = self.computer_color if color == self.player_color else self.player_color
        opponent_pieces = len([piece for piece in self.board.pieces if piece.color == opponent_color])

        # Calculate the score difference
        score_difference = winner_pieces - opponent_pieces
        self.player_scores[player_number - 1] += score_difference

        # Update rounds won
        self.player_wins[player_number - 1] += 1

        # Update the color of the previous winner
        self.previous_winner_color = color

        # Log the updated scores and rounds won
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
        print("Asking the user if they want to replay...")  # Debugging
        popup_width, popup_height = 400, 200
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Play Again?")

        font = pygame.font.SysFont('Arial', 24)
        prompt_surface = font.render("Play Again?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(popup_width // 2, popup_height // 2 - 30))

        yes_button_rect = pygame.Rect(popup_width // 2 - 60, popup_height // 2 + 20, 50, 30)
        no_button_rect = pygame.Rect(popup_width // 2 + 10, popup_height // 2 + 20, 50, 30)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button_rect.collidepoint(event.pos):
                        print("User chose to replay.")  # Debugging
                        self.reset_game()  # Reset game state
                        running = False  # Exit the loop
                    elif no_button_rect.collidepoint(event.pos):
                        print("User chose not to replay. Exiting...")  # Debugging
                        pygame.quit()
                        exit()

            popup_window.fill((240, 240, 240))
            popup_window.blit(prompt_surface, prompt_rect)

            pygame.draw.rect(popup_window, (0, 255, 0), yes_button_rect)  # Green for Yes
            pygame.draw.rect(popup_window, (255, 0, 0), no_button_rect)  # Red for No

            yes_text = font.render("Yes", True, (0, 0, 0))
            no_text = font.render("No", True, (0, 0, 0))

            popup_window.blit(yes_text, yes_button_rect.move(5, 0))
            popup_window.blit(no_text, no_button_rect.move(10, 0))

            pygame.display.flip()

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
    Reference: None
    """

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        board_offset = self.board.offset
        grid_size = self.board.grid_size

        if x < board_offset or y < board_offset:
            return None, None

        row = (y - board_offset) // grid_size
        col = (x - board_offset) // grid_size

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
        piece = self.board.get_piece(row, col)
        if piece and self.is_correct_turn(piece):
            print(f"Selected piece at {row}, {col} for {self.get_color_name(piece.color)}.")  # Debugging
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
        if self.selected_piece:
            start_row = self.selected_piece.row
            start_col = self.selected_piece.col

            is_valid, message = self.board.is_valid_move(self.selected_piece, row, col)
            if is_valid:
                print(f"Moving piece from {start_row}, {start_col} to {row}, {col}.")  # Debugging
                self.add_to_move_history(self.selected_piece, start_row, start_col, row, col)
                self.board.move_piece(self.selected_piece, row, col)
                self.end_turn()
                self.error_message = ""
            else:
                print(f"Invalid move attempted: {message}")  # Debugging
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
        self.selected_piece = None
        # Increment the current turn to the next player
        self.current_turn = (self.current_turn + 1) % self.num_players
        print(f"Turn ended. Next player's turn: {self.current_turn}")  # Debugging statement

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
        if self.num_players == 2:
            if self.current_turn == 0:  # Player's turn
                return piece.color == self.player_color
            else:  # Computer's turn
                return piece.color == self.computer_color
        else:
            # 4-player mode logic
            current_color = \
                [(player, color) for player, color in self.player_colors.items() if player == self.current_turn + 1][0][
                    1]
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
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)

        # Determine the player number and color
        player_number = self.get_player_number(piece.color)
        color_name = self.get_color_name(piece.color)

        # Construct a descriptive move message
        move = f"Player {player_number} ({color_name}) moved {start_notation} to {end_notation}"
        self.move_history.append(move)
        print(f"Move added to history: {move}")  # Debugging

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
        pygame.draw.rect(self.window, (0, 0, 0), self.save_game_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Save Game", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.save_game_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

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
            with open(save_file_path, 'w') as save_file:
                # Write board state
                save_file.write("Board:\n")
                for row in range(self.board.rows):
                    for col in range(self.board.cols):
                        piece = self.board.get_piece(row, col)
                        if piece:
                            # Save piece color ('B' for black, 'W' for white, etc.)
                            piece_symbol = self.get_color_symbol(piece.color)
                        else:
                            # Empty spaces represented by '.'
                            piece_symbol = '.'
                        save_file.write(piece_symbol + ' ')
                    save_file.write('\n')

                # Write player information (for 2-player mode)
                if self.num_players == 2:
                    save_file.write("\nPlayers:\n")
                    save_file.write("Player 1 Color: " + self.get_color_name(self.player_color) + "\n")
                    save_file.write("Player 2 Color: " + self.get_color_name(self.computer_color) + "\n")

                # Write move history
                save_file.write("\nMove History:\n")
                for move in self.move_history:
                    save_file.write(move + "\n")

                # Write current turn
                save_file.write("\nCurrent Turn: Player " + str(self.current_turn + 1) + "\n")

            print("Game state saved successfully.")
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
        if color == (0, 0, 0):
            return 'B'  # Black
        elif color == (255, 255, 255):
            return 'W'  # White
        elif color == (255, 0, 0):
            return 'R'  # Red
        elif color == (0, 255, 0):
            return 'G'  # Green
        else:
            return '.'  # Unknown color or empty

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
        file_path = f"game_case_{case_number}.txt"

        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found.")
            return

        try:
            with open(file_path, 'r') as load_file:
                lines = load_file.readlines()
                print(f"Loaded lines: {lines}")  # Debugging statement

                # Initialize the board and clear it
                self.board = Board(self.board_size, initialize=False)
                self.board.clear_board()  # This now works with the corrected method
                print("Initializing board from loaded state...")

                # Load the board state
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

                # Determine who is who
                if next_player_line == "Computer":
                    # If the computer is the next player
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

                # Create players after setting player colors
                self.players = self.create_players()

                print("Game state loaded successfully.")
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
        pygame.draw.rect(self.window, (0, 0, 0), self.help_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Help", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.help_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

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
        possible_moves, capture_moves = self.generate_human_player_moves()

        # Create a popup window to display the help information
        popup_width, popup_height = 400, 600
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Help - Possible Moves")

        font = pygame.font.SysFont('Arial', 20)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            popup_window.fill((240, 240, 240))

            y_position = 20
            if capture_moves:
                capture_title = font.render("Capture Moves:", True, (0, 0, 0))
                popup_window.blit(capture_title, (20, y_position))
                y_position += 30
                for move in capture_moves:
                    move_surface = font.render(move, True, (0, 0, 0))
                    popup_window.blit(move_surface, (20, y_position))
                    y_position += move_surface.get_height() + 5

            if possible_moves:
                non_capture_title = font.render("Possible Moves:", True, (0, 0, 0))
                popup_window.blit(non_capture_title, (20, y_position))
                y_position += 30
                for move in possible_moves:
                    move_surface = font.render(move, True, (0, 0, 0))
                    popup_window.blit(move_surface, (20, y_position))
                    y_position += move_surface.get_height() + 5

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
        possible_moves = []
        capture_moves = []
        color = self.player_color if self.current_turn == 0 else self.computer_color  # Get the current player's color

        # Iterate through all pieces on the board
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    # Generate moves for this piece
                    moves, captures = self.generate_moves_for_piece(row, col)
                    possible_moves.extend(moves)
                    capture_moves.extend(captures)

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
        moves = []
        captures = []
        piece = self.board.get_piece(start_row, start_col)

        # Horizontal, Vertical, and Diagonal moves
        # Use logic similar to the ComputerPlayer to generate moves
        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)

        # Horizontal moves
        for offset in range(1, horizontal_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col + offset, moves, captures)  # Right
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col - offset, moves, captures)  # Left

        # Vertical moves
        for offset in range(1, vertical_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col, moves, captures)  # Down
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col, moves, captures)  # Up

        # Diagonal moves
        for offset in range(1, diagonal_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col + offset, moves,
                                         captures)  # Bottom-right
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col - offset, moves,
                                         captures)  # Top-left
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col - offset, moves,
                                         captures)  # Bottom-left
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col + offset, moves,
                                         captures)  # Top-right

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
        if 0 <= end_row < self.board.rows and 0 <= end_col < self.board.cols:
            is_valid, captures_list = self.validate_move(start_row, start_col, end_row, end_col)
            start_notation = self.board.get_position_notation(start_row, start_col)
            end_notation = self.board.get_position_notation(end_row, end_col)
            move = f"{start_notation} to {end_notation}"
            if is_valid:
                if captures_list:
                    captures.append(move)
                else:
                    moves.append(move)

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
        captures = []
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.player_color:  # Only validate for pieces controlled by the human player
            return False, captures

        # Use the board's existing move validation logic
        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.player_color:
                captures.append((end_row, end_col))
            return True, captures

        return False, captures

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
        if self.num_players == 2:
            # For 2-player mode, determine if it's the human or the computer's turn
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            # Get the color of the player whose turn it is (human or computer)
            color = self.player_color if self.current_turn == 0 else self.computer_color
            # Get the color name (e.g., "Black" or "White") for display
            color_name = self.get_color_name(color)
        else:
            # For 4-player mode, determine the current player's number (1-based)
            player_number = self.current_turn + 1
            # Determine if the current player is a human or computer
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            # Get the color assigned to the current player
            color = self.player_colors[player_number]
            # Get the color name (e.g., "Black", "Red") for display
            color_name = self.get_color_name(color)

        # Construct the message showing which player's turn it is
        turn_text = f"{player_type} (Player {self.current_turn + 1}, {color_name})'s turn"

        # Set up font and render the text message in black
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(turn_text, True, (0, 0, 0))  # Black text
        # Display the message at the top center of the game window (positioned at x=300, y=10)
        self.window.blit(text_surface, (300, 10))
        pygame.display.update()  # Update the display to show the current player's turn

        # If it's the computer's turn, add a brief pause to ensure the player can see the message
        if player_type == "Computer":
            pygame.time.wait(500)  # Wait for 500 milliseconds before the computer moves


