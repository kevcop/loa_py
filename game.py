import pygame
from board import Board
from menu import Menu
from piece import Piece
from computerPlayer import ComputerPlayer  # AI class
from HumanPlayer import HumanPlayer
import os
import time


class Game:
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

    def reset_game(self):
        """Resets all necessary game variables for a new round."""
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

    def create_players(self):
        """Creates the players for the game based on the number of players and their types."""
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

    def update(self):
        """Update the game state and handle rendering."""
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

    def display_error_message(self):
        """Displays any error messages (e.g., invalid moves)."""
        if self.error_message:
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.error_message, True, (255, 0, 0))
            self.window.blit(text_surface, (10, 10))

    def display_show_history_button(self):
        """Displays a button to show move history."""
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Show History", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)
        self.window.blit(text_surface, text_rect)

    def handle_click(self, pos):
        """Handles mouse clicks during the game."""
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

    def show_move_history_popup(self):
        """Displays the move history in a popup window."""
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

    def check_winner(self):
        """Checks if a player has won by forming a connected group of pieces."""
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

    def display_winner(self, color):
        """Displays the winner in a popup window and shows scores and rounds won."""
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

    def get_player_number(self, color):
        """Returns the player number corresponding to the given color."""
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

    def update_score(self, player_number, color):
        """Updates the score for the player who won the round."""
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

    def ask_replay(self):
        """Prompts the player to replay the game or quit."""
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

    def get_row_col_from_mouse(self, pos):
        """Returns the row and column based on mouse click position."""
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

    def select_piece(self, row, col):
        """Handles selecting a piece on the board."""
        piece = self.board.get_piece(row, col)
        if piece and self.is_correct_turn(piece):
            print(f"Selected piece at {row}, {col} for {self.get_color_name(piece.color)}.")  # Debugging
            self.selected_piece = piece
            self.error_message = ""  # Clear error message when a piece is successfully selected

    def move_piece(self, row, col):
        """Handles moving a selected piece."""
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

    def end_turn(self):
        """Ends the current player's turn and switches to the next player."""
        self.selected_piece = None
        # Increment the current turn to the next player
        self.current_turn = (self.current_turn + 1) % self.num_players
        print(f"Turn ended. Next player's turn: {self.current_turn}")  # Debugging statement

    def is_correct_turn(self, piece):
        """Checks if it's the correct player's turn to move the selected piece."""
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

    def add_to_move_history(self, piece, start_row, start_col, end_row, end_col):
        """Adds the current move to the move history with a descriptive message."""
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)

        # Determine the player number and color
        player_number = self.get_player_number(piece.color)
        color_name = self.get_color_name(piece.color)

        # Construct a descriptive move message
        move = f"Player {player_number} ({color_name}) moved {start_notation} to {end_notation}"
        self.move_history.append(move)
        print(f"Move added to history: {move}")  # Debugging

    def get_color_name(self, color):
        """Convert an RGB color tuple to a string representing the color name."""
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

    def display_save_game_button(self):
        """Displays the 'Save Game' button."""
        pygame.draw.rect(self.window, (0, 0, 0), self.save_game_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Save Game", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.save_game_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

    def save_game_state(self):
        """Saves the current state of the game to a file."""
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

    def get_color_symbol(self, color):
        """Returns a single-character symbol representing the piece color."""
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

    def load_game_state(self, case_number):
        """Loads a saved game state from a file."""
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

    def display_help_button(self):
        """Displays the 'Help' button."""
        pygame.draw.rect(self.window, (0, 0, 0), self.help_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Help", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.help_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

    def display_help(self):
        """Displays all possible valid moves for the human player."""
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

    def generate_human_player_moves(self):
        """Generates all possible valid moves for the human player."""
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

    def generate_moves_for_piece(self, start_row, start_col):
        """Generates valid moves for a specific piece."""
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

    def add_human_move_if_valid(self, start_row, start_col, end_row, end_col, moves, captures):
        """Adds a move to the list if it's valid."""
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

    def validate_move(self, start_row, start_col, end_row, end_col):
        """Validates if a move is allowed and checks for captures."""
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
