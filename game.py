# game.py

import pygame
from board import Board
from computerPlayer import ComputerPlayer

class Game:
    def __init__(self, window, num_players, players_type):
        self.window = window
        self.num_players = num_players
        self.players_type = players_type
        self.computer_players = []  # List to hold the AI players
        self.current_turn = 0  # To track which player's turn it is (index 0 to num_players - 1)
        self.reset_game()

    def reset_game(self):
        self.board = Board()
        self.selected_piece = None
        self.error_message = ""  # To store error messages
        self.move_history = []  # List to store move history
        self.history_font = pygame.font.SysFont('Arial', 20)
        self.history_box_height = 150  # Height of the move history box
        self.history_offset = 10  # Padding within the history box
        self.show_history_button_rect = pygame.Rect(650, 20, 140, 50)  # Button to show move history
        self.winner_displayed = False  # Track if the winner has been displayed

        # Initialize AI players if any
        self.computer_players = []
        for i, player_type in enumerate(self.players_type):
            if player_type == "Computer":
                color = "white" if i % 2 != 0 else "black"
                self.computer_players.append(ComputerPlayer(self.board, color))
            else:
                self.computer_players.append(None)  # No AI for human players

    def update(self):
        self.window.fill((255, 255, 255))  # Fill the screen with white
        self.board.draw(self.window, self.selected_piece)  # Draw the board and pieces
        self.display_error_message()
        self.display_show_history_button()

        # Check if the current player is an AI, and make the AI move
        if isinstance(self.computer_players[self.current_turn], ComputerPlayer):
            self.computer_players[self.current_turn].make_move()
            self.end_turn()

        # Check for a winner
        if not self.winner_displayed:
            self.check_winner()

    def display_error_message(self):
        if self.error_message:
            font = pygame.font.SysFont('Arial', 24)
            text_surface = font.render(self.error_message, True, (255, 0, 0))
            self.window.blit(text_surface, (10, 10))

    def display_show_history_button(self):
        pygame.draw.rect(self.window, (0, 0, 0), self.show_history_button_rect)
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render("Show History", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.show_history_button_rect.center)
        self.window.blit(text_surface, text_rect)

    def handle_click(self, pos):
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
        if self.board.check_connected_group((0, 0, 0)):
            self.display_winner("Black")
        elif self.board.check_connected_group((255, 255, 255)):
            self.display_winner("White")

    def display_winner(self, color):
        # Create a popup window to display the winner
        popup_width, popup_height = 300, 200
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Game Over")

        font = pygame.font.SysFont('Arial', 30)
        text_surface = font.render(f"{color} Wins!", True, (0, 0, 0))
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

        # Ask if the player wants to play again
        self.ask_replay()

    def ask_replay(self):
        # Create a popup window to ask for replay
        popup_width, popup_height = 400, 200
        popup_window = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Play Again?")

        font = pygame.font.SysFont('Arial', 24)
        prompt_surface = font.render("Play Again?", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect(center=(popup_width // 2, popup_height // 2 - 30))

        # Define Yes/No buttons
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
                        self.reset_game()  # Reset the game if "Yes" is pressed
                        running = False
                    elif no_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()  # Exit the game if "No" is pressed

            popup_window.fill((240, 240, 240))
            popup_window.blit(prompt_surface, prompt_rect)

            # Draw Yes/No buttons
            pygame.draw.rect(popup_window, (0, 255, 0), yes_button_rect)  # Green for Yes
            pygame.draw.rect(popup_window, (255, 0, 0), no_button_rect)  # Red for No

            yes_text = font.render("Yes", True, (0, 0, 0))
            no_text = font.render("No", True, (0, 0, 0))

            popup_window.blit(yes_text, yes_button_rect.move(5, 0))
            popup_window.blit(no_text, no_button_rect.move(10, 0))

            pygame.display.flip()

        # Restore the main game window after the popup is closed
        self.window = pygame.display.set_mode((800, 800))

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        board_offset = self.board.offset
        grid_size = self.board.grid_size

        # Adjust for the offset
        if x < board_offset or y < board_offset:
            return None, None  # Click is outside the board grid

        row = (y - board_offset) // grid_size
        col = (x - board_offset) // grid_size

        # Ensure the click is within the bounds of the board
        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            return row, col
        return None, None

    def select_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and self.is_correct_turn(piece):
            self.selected_piece = piece
            self.error_message = ""  # Clear error message when a piece is successfully selected

    def move_piece(self, row, col):
        if self.selected_piece:
            start_row = self.selected_piece.row
            start_col = self.selected_piece.col

            is_valid, message = self.board.is_valid_move(self.selected_piece, row, col)
            if is_valid:
                self.add_to_move_history(self.selected_piece, start_row, start_col, row,
                                         col)  # Add the move to history before moving the piece
                self.board.move_piece(self.selected_piece, row, col)
                self.end_turn()
                self.error_message = ""  # Clear error message on a successful move
            else:
                self.error_message = message
                self.selected_piece = None  # Deselect piece on invalid move

    def end_turn(self):
        self.selected_piece = None
        self.current_turn = (self.current_turn + 1) % self.num_players  # Rotate to the next player

    def is_correct_turn(self, piece):
        piece_color = (0, 0, 0) if self.current_turn % 2 == 0 else (255, 255, 255)
        return piece.color == piece_color

    def add_to_move_history(self, piece, start_row, start_col, end_row, end_col):
        start_notation = self.board.get_position_notation(start_row, start_col)
        end_notation = self.board.get_position_notation(end_row, end_col)
        move = f"{start_notation} to {end_notation}"
        self.move_history.append(move)

        # Auto-scroll down to the latest move
        total_height = len(self.move_history) * (self.history_font.get_height() + 5)
        visible_height = self.history_box_height - 2 * self.history_offset
        if total_height > visible_height:
            self.history_scroll_offset = total_height - visible_height