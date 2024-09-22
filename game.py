import pygame
from board import Board
from menu import Menu
from piece import Piece
from computerPlayer import ComputerPlayer  # AI class
from HumanPlayer import HumanPlayer
import os
import time


class Game:
    """
    Manages the main gameplay of Lines of Action.

    This class handles initializing the board, managing turns, keeping track of move history,
    and saving or loading game states.
    """

    def __init__(self, window, num_players, players_type, player_order=None, player_colors=None, board_size=None,
                 player_color=None, computer_color=None, case=None):
        """
        Initializes the game with the provided settings.

        Args:
            window (pygame.Surface): The game window.
            num_players (int): The number of players (2 or 4).
            players_type (list): List specifying whether each player is human or computer.
            player_order (list): The order in which players take turns (optional).
            player_colors (dict): A dictionary mapping player numbers to their colors (optional).
            board_size (int): The size of the board.
            player_color (tuple): RGB color of the player for 2-player mode.
            computer_color (tuple): RGB color of the computer for 2-player mode.
            case (int): The number of the saved game case to load (optional).
        """
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
        """
        Resets all necessary game variables for a new round.

        This includes reinitializing the board, resetting players, and setting the initial turn.
        """
        print("Resetting the game for a new round...")  # Debugging

        self.winner_displayed = False
        print(f"Winner flag reset: {self.winner_displayed}")  # Debugging

        # Reinitialize the board and verify it has no pieces
        self.board = Board(self.board_size)
        print("New board initialized with size", self.board_size)  # Debugging
        print(f"Board state after reset: {self.board.pieces}")  # Debugging

        self.selected_piece = None
        self.error_message = ""
        self.move_history = []
        self.players = self.create_players()  # Recreate players for the new game
        print(f"Players created: {self.players}")  # Debugging

        if self.num_players == 2:
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
        """
        Creates the players for the game based on the number of players and their types.

        Returns:
            list: A list of player objects (either HumanPlayer or ComputerPlayer).
        """
        players = []
        print("Creating players...")  # Debugging

        if self.num_players == 2:
            colors = [self.player_color, self.computer_color]
            print(f"2-player game with colors: {colors}")  # Debugging
            for i in range(self.num_players):
                if self.players_type[i] == "Computer":
                    print(f"Player {i + 1} is a computer.")  # Debugging
                    players.append(ComputerPlayer(self.board, colors[i]))  # AI player
                else:
                    print(f"Player {i + 1} is a human.")  # Debugging
                    players.append(HumanPlayer())  # Use HumanPlayer class
        else:
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
        """
        Updates the game state and renders the game elements.

        Handles turn updates, rendering the board, and determining if the game has a winner.
        """
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

        if not self.winner_displayed:
            print("Checking for a winner...")  # Debugging
            self.check_winner()
        else:
            print("Winner has already been displayed, skipping winner check.")  # Debugging

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
            print(f"Human player {self.current_turn + 1}'s turn.")  # Debugging

    def display_error_message(self):
        """
        Displays any error messages (e.g., invalid moves).
        """
        if self.error_message:
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.error_message, True, (255, 0, 0))
            self.window.blit(text_surface, (10, 10))

    def display_show_history_button(self):
        """
        Displays a button to show move history.
        """
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Show History", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)
        self.window.blit(text_surface, text_rect)

    def handle_click(self, pos):
        """
        Handles mouse clicks during the game.

        Args:
            pos (tuple): The (x, y) position of the mouse click.
        """
        if self.show_history_button_rect.collidepoint(pos):
            self.show_move_history_popup()  # Show move history when the button is clicked
        elif self.save_game_button_rect.collidepoint(pos):
            self.save_game_state()  # Save the game when the button is clicked
        elif self.help_button_rect.collidepoint(pos):
            self.display_help()  # Display help for the human player when the Help button is clicked
        else:
            row, col = self.get_row_col_from_mouse(pos)
            if row is not None and col is not None:
                if self.selected_piece:
                    self.move_piece(row, col)
                else:
                    self.select_piece(row, col)

    def show_move_history_popup(self):
        """
        Displays the move history in a popup window.
        """
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

        self.window = pygame.display.set_mode((800, 800))

    def check_winner(self):
        """
        Checks if a player has won by forming a connected group of pieces.
        """
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
                    self.winner_displayed = True
                    print(f"Winner flag set to {self.winner_displayed} after finding winner")  # Debugging
                    break
            else:
                print("No winner found yet.")  # Debugging

    def display_winner(self, color):
        """
        Displays the winner in a popup window and shows scores and rounds won.

        Args:
            color (tuple): The RGB color of the winning player.
        """
        print(f"Displaying winner: {self.get_color_name(color)}")  # Debugging
        player_number = self.get_player_number(color)

        self.update_score(player_number, color)

        popup_width, popup_height = 400, 300
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Game Over")

        font = pygame.font.SysFont('Arial', 30)
        color_name = self.get_color_name(color)
        text_surface = font.render(f"Player {player_number} ({color_name}) Wins!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_width // 2, 50))

        info_font = pygame.font.SysFont('Arial', 20)

        scores_text = [f"Player {i + 1} - Rounds Won: {self.player_wins[i]}, Score: {self.player_scores[i]}"
                       for i in range(self.num_players)]
        scores_surfaces = [info_font.render(score_text, True, (0, 0, 0)) for score_text in scores_text]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

            popup_window.fill((240, 240, 240))
            popup_window.blit(text_surface, text_rect)

            y_offset = 100
            for surface in scores_surfaces:
                popup_window.blit(surface, (20, y_offset))
                y_offset += 30

            pygame.display.flip()

        self.ask_replay()

    def get_player_number(self, color):
        """
        Returns the player number corresponding to the given color.

        Args:
            color (tuple): The RGB color of the player.

        Returns:
            int: The player number associated with the color.
        """
        if self.num_players == 2:
            if color == self.player_color:
                return 1  # Player 1
            elif color == self.computer_color:
                return 2  # Player 2 (Computer)
        else:
            for player_num, player_color in self.player_colors.items():
                if player_color == color:
                    return player_num
        return "Unknown"

    def update_score(self, player_number, color):
        """
        Updates the score for the player who won the round.

        Args:
            player_number (int): The number of the player who won.
            color (tuple): The RGB color of the winning player.
        """
        winner_pieces = len([piece for piece in self.board.pieces if piece.color == color])
        opponent_color = self.computer_color if color == self.player_color else self.player_color
        opponent_pieces = len([piece for piece in self.board.pieces if piece.color == opponent_color])

        score_difference = winner_pieces - opponent_pieces
        self.player_scores[player_number - 1] += score_difference

        self.player_wins[player_number - 1] += 1

        self.previous_winner_color = color

        print(f"Updated Score for Player {player_number}: {self.player_scores[player_number - 1]}")
        print(f"Rounds Won by Player {player_number}: {self.player_wins[player_number - 1]}")

    def ask_replay(self):
        """
        Prompts the player to replay the game or quit.
        """
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
                        self.reset_game()
                        running = False
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
        """
        Returns the row and column based on mouse click position.

        Args:
            pos (tuple): The (x, y) position of the mouse click.

        Returns:
            tuple: The row and column corresponding to the mouse position.
        """
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
        """
        Handles selecting a piece on the board.

        Args:
            row (int): The row of the selected piece.
            col (int): The column of the selected piece.
        """
        piece = self.board.get_piece(row, col)
        if piece and self.is_correct_turn(piece):
            print(f"Selected piece at {row}, {col} for {self.get_color_name(piece.color)}.")  # Debugging
            self.selected_piece = piece
            self.error_message = ""  # Clear error message when a piece is successfully selected

    def move_piece(self, row, col):
        """
        Handles moving a selected piece.

        Args:
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """
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
        """
        Ends the current player's turn and switches to the next player.
        """
        self.selected_piece = None
        self.current_turn = (self.current_turn + 1) % self.num_players
        print(f"Turn ended. Next player's turn: {self.current_turn}")  # Debugging

    def is_correct_turn(self, piece):
        """
        Checks if it's the correct player's turn to move the selected piece.

        Args:
            piece (Piece): The selected piece.

        Returns:
            bool: True if it's the correct turn for the piece, False otherwise.
        """
        if self.num_players == 2:
            if self.current_turn == 0:
                return piece.color == self.player_color
            else:
                return piece.color == self.computer_color
        else:
            current_color = \
                [(player, color) for player, color in self.player_colors.items() if player == self.current_turn + 1][0][
                    1]
            return piece.color == current_color

    def add_to_move_history(self, piece, start_row, start_col, end_row, end_col):
        """
        Adds the current move to the move history with a descriptive message.

        Args:
            piece (Piece): The piece being moved.
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.
            end_row (int): The ending row of the piece.
            end_col (int): The ending column of the piece.
        """
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)

        player_number = self.get_player_number(piece.color)
        color_name = self.get_color_name(piece.color)

        move = f"Player {player_number} ({color_name}) moved {start_notation} to {end_notation}"
        self.move_history.append(move)
        print(f"Move added to history: {move}")  # Debugging

    def get_color_name(self, color):
        """
        Convert an RGB color tuple to a string representing the color name.

        Args:
            color (tuple): The RGB color of the piece.

        Returns:
            str: The name of the color.
        """
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
        """
        Displays the 'Save Game' button.
        """
        pygame.draw.rect(self.window, (0, 0, 0), self.save_game_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Save Game", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.save_game_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

    def save_game_state(self):
        """
        Saves the current state of the game to a file.
        """
        save_file_path = "game_state.txt"

        try:
            with open(save_file_path, 'w') as save_file:
                save_file.write("Board:\n")
                for row in range(self.board.rows):
                    for col in range(self.board.cols):
                        piece = self.board.get_piece(row, col)
                        if piece:
                            piece_symbol = self.get_color_symbol(piece.color)
                        else:
                            piece_symbol = '.'
                        save_file.write(piece_symbol + ' ')
                    save_file.write('\n')

                if self.num_players == 2:
                    save_file.write("\nPlayers:\n")
                    save_file.write("Player 1 Color: " + self.get_color_name(self.player_color) + "\n")
                    save_file.write("Player 2 Color: " + self.get_color_name(self.computer_color) + "\n")

                save_file.write("\nMove History:\n")
                for move in self.move_history:
                    save_file.write(move + "\n")

                save_file.write("\nCurrent Turn: Player " + str(self.current_turn + 1) + "\n")

            print("Game state saved successfully.")
        except Exception as e:
            print(f"Error saving game state: {e}")

    def get_color_symbol(self, color):
        """
        Returns a single-character symbol representing the piece color.

        Args:
            color (tuple): The RGB color of the piece.

        Returns:
            str: A single-character symbol for the color.
        """
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
        """
        Loads a saved game state from a file.

        Args:
            case_number (int): The number of the saved game case to load.
        """
        file_path = f"game_case_{case_number}.txt"

        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found.")
            return

        try:
            with open(file_path, 'r') as load_file:
                lines = load_file.readlines()
                print(f"Loaded lines: {lines}")  # Debugging statement

                self.board = Board(self.board_size, initialize=False)
                self.board.clear_board()  # This now works with the corrected method
                print("Initializing board from loaded state...")

                board_section = lines[1:self.board_size + 1]
                for row, line in enumerate(board_section):
                    pieces = line.strip().split()
                    for col, piece_symbol in enumerate(pieces):
                        piece_symbol = piece_symbol.upper()
                        if piece_symbol == 'B':
                            color_rgb = (0, 0, 0)  # Black piece RGB
                            self.board.set_piece(row, col, color_rgb)
                        elif piece_symbol == 'W':
                            color_rgb = (255, 255, 255)  # White piece RGB
                            self.board.set_piece(row, col, color_rgb)

                next_player_line = lines[-2].strip().split(": ")[1]
                next_color_line = lines[-1].strip().split(": ")[1]

                if next_player_line == "Computer":
                    if next_color_line == "Black":
                        self.computer_color = (0, 0, 0)
                        self.player_color = (255, 255, 255)
                    else:
                        self.computer_color = (255, 255, 255)
                        self.player_color = (0, 0, 0)
                    self.current_turn = 1  # Computer's turn
                else:
                    if next_color_line == "Black":
                        self.player_color = (0, 0, 0)
                        self.computer_color = (255, 255, 255)
                    else:
                        self.player_color = (255, 255, 255)
                        self.computer_color = (0, 0, 0)
                    self.current_turn = 0  # Human's turn

                print(f"Player color set to: {self.get_color_name(self.player_color)}")
                print(f"Computer color set to: {self.get_color_name(self.computer_color)}")
                print(f"Current turn set to: {self.current_turn}")

                self.players = self.create_players()

                print("Game state loaded successfully.")
        except Exception as e:
            print(f"Error loading game state: {e}")

    def display_help_button(self):
        """
        Displays the 'Help' button.
        """
        pygame.draw.rect(self.window, (0, 0, 0), self.help_button_rect)  # Draw button rectangle
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Help", True, (255, 255, 255))  # Button text
        text_rect = text_surface.get_rect(center=self.help_button_rect.center)
        self.window.blit(text_surface, text_rect)  # Render the button text onto the window

    def display_help(self):
        """
        Displays all possible valid moves for the human player.
        """
        possible_moves, capture_moves = self.generate_human_player_moves()

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

        self.window = pygame.display.set_mode((800, 800))

    def generate_human_player_moves(self):
        """
        Generates all possible valid moves for the human player.

        Returns:
            tuple: A tuple containing lists of possible moves and capture moves.
        """
        possible_moves = []
        capture_moves = []
        color = self.player_color if self.current_turn == 0 else self.computer_color

        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    moves, captures = self.generate_moves_for_piece(row, col)
                    possible_moves.extend(moves)
                    capture_moves.extend(captures)

        return possible_moves, capture_moves

    def generate_moves_for_piece(self, start_row, start_col):
        """
        Generates valid moves for a specific piece.

        Args:
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.

        Returns:
            tuple: A tuple containing lists of valid moves and capture moves.
        """
        moves = []
        captures = []
        piece = self.board.get_piece(start_row, start_col)

        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)

        for offset in range(1, horizontal_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col + offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row, start_col - offset, moves, captures)

        for offset in range(1, vertical_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col, moves, captures)

        for offset in range(1, diagonal_moves_required + 1):
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col + offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col - offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row + offset, start_col - offset, moves, captures)
            self.add_human_move_if_valid(start_row, start_col, start_row - offset, start_col + offset, moves, captures)

        return moves, captures

    def add_human_move_if_valid(self, start_row, start_col, end_row, end_col, moves, captures):
        """
        Adds a move to the list if it's valid.

        Args:
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.
            end_row (int): The ending row of the move.
            end_col (int): The ending column of the move.
            moves (list): The list of valid moves.
            captures (list): The list of capture moves.
        """
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
        """
        Validates if a move is allowed and checks for captures.

        Args:
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.
            end_row (int): The ending row of the move.
            end_col (int): The ending column of the move.

        Returns:
            tuple: A tuple containing a boolean indicating validity and a list of captures.
        """
        captures = []
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.player_color:
            return False, captures

        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.player_color:
                captures.append((end_row, end_col))
            return True, captures

        return False, captures

    def display_current_player(self):
        """
        Displays which player's turn it is on the game screen.
        """
        if self.num_players == 2:
            # In 2-player mode, determine whether it's the human or computer's turn.
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            color = self.player_color if self.current_turn == 0 else self.computer_color
            color_name = self.get_color_name(color)
        else:
            # In 4-player mode, determine which player is currently taking their turn.
            player_number = self.current_turn + 1  # 1-based player number
            player_type = "Computer" if isinstance(self.players[self.current_turn], ComputerPlayer) else "Player"
            color = self.player_colors[player_number]
            color_name = self.get_color_name(color)

        # Create the message to display whose turn it is
        turn_text = f"{player_type} (Player {self.current_turn + 1}, {color_name})'s turn"

        # Render the message to be displayed at the top of the window
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(turn_text, True, (0, 0, 0))  # Black text
        self.window.blit(text_surface, (300, 10))  # Display at the top-center of the screen
        pygame.display.update()

        # Short pause to make sure the message is visible before the computer moves
        if player_type == "Computer":
            pygame.time.wait(500)  # Adjust this wait time as needed


