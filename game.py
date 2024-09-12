import pygame
from board import Board
from computerPlayer import ComputerPlayer  # AI class


class Game:
    def __init__(self, window, num_players, players_type, player_order=None, player_colors=None, board_size=None,
                 player_color=None, computer_color=None):
        self.window = window
        self.num_players = num_players
        self.players_type = players_type
        self.player_order = player_order
        self.player_colors = player_colors
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
        self.winner_displayed = False  # Track if the winner has been displayed
        self.players = []  # List to store the players (Human or AI)
        print(f"Initializing game with {num_players} players.")  # Debugging player count

        # Initialize the game
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

        # Reset move history and error messages
        print("Move history cleared, and error messages reset.")

        # Ensure proper first turn setup for 2-player or 4-player mode
        if self.num_players == 2:
            if self.player_color == (0, 0, 0):  # Black
                self.current_turn = 0  # Player moves first
                print("Player (Black) moves first.")
            else:
                self.current_turn = 1  # Computer moves first
                print("Computer (White) moves first.")
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
                    players.append(None)  # Human player (we handle human moves manually)
        else:
            # In 4-player mode, use player_colors (which is a dictionary with keys 1-4)
            for i in range(1, self.num_players + 1):  # 1-based index for 4-player
                if self.players_type[i - 1] == "Computer":
                    print(f"Player {i} is a computer. Color: {self.player_colors[i]}")  # Debugging
                    players.append(ComputerPlayer(self.board, self.player_colors[i]))  # AI player
                else:
                    print(f"Player {i} is a human. Color: {self.player_colors[i]}")  # Debugging
                    players.append(None)  # Human player (we handle human moves manually)

        return players

    def update(self):
        """Update the game state and handle rendering."""
        print("Game update running...")  # Add this debug statement to ensure update() is being called
        print(f"Winner flag before update: {self.winner_displayed}")  # Debugging
        self.winner_displayed = False
        self.window.fill((255, 255, 255))  # Fill the screen with white
        self.board.draw(self.window, self.selected_piece)  # Draw the board and pieces
        self.display_error_message()
        self.display_show_history_button()

        # Check for a winner
        if not self.winner_displayed:
            print("Checking for a winner...")  # Debugging
            self.check_winner()
        else:
            print("Winner has already been displayed, skipping winner check.")  # Debugging

        # If it's an AI's turn, make the move
        if isinstance(self.players[self.current_turn], ComputerPlayer):
            print(f"Computer player {self.current_turn + 1} is making a move...")  # Debugging
            self.players[self.current_turn].make_move()
            self.end_turn()  # Move to the next player after the AI move

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
            self.show_move_history_popup()
        else:
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
        """Displays the winner in a popup window."""
        print(f"Displaying winner: {self.get_color_name(color)}")  # Debugging
        popup_width, popup_height = 300, 200
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Game Over")

        font = pygame.font.SysFont('Arial', 30)
        color_name = self.get_color_name(color)
        text_surface = font.render(f"{color_name} Wins!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_width // 2, popup_height // 2))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False  # Close the popup when Enter is pressed

            popup_window.fill((240, 240, 240))
            popup_window.blit(text_surface, text_rect)
            pygame.display.flip()

        self.ask_replay()

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
        #print(f"Ending turn for player {self.current_turn + 1}.")  # Debugging
        self.selected_piece = None
        self.current_turn = (self.current_turn + 1) % self.num_players
        #print(f"Next player's turn: Player {self.current_turn + 1}.")  # Debugging

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
            [(player, color) for player, color in self.player_colors.items() if player == self.current_turn + 1][0][1]
            return piece.color == current_color

    def add_to_move_history(self, piece, start_row, start_col, end_row, end_col):
        """Adds the current move to the move history."""
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)
        move = f"{start_notation} to {end_notation}"
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
