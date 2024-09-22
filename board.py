import pygame
from piece import Piece



class Board:
    """
    Represents the game board for the Lines of Action game.

    This class manages the state of the game board, including piece positions,
    validating moves, and tracking the number of pieces.

    PROVIDE PICS WITH FIXED GAME
    """

    def __init__(self, size, initialize=True):
        """
        Constructor to initialize the game board.

        Initializes the game board with the given size and optionally places
        pieces on the board.

        Args:
            size (int): The size of the board (number of rows and columns).
            initialize (bool): A flag indicating whether to initialize pieces.
        """
        self.rows = size
        self.cols = size
        self.window_size = 800  # Fixed window size
        self.offset = 50  # Offset for labels
        self.grid_size = (
                                     self.window_size - self.offset * 2) // size  # Dynamically calculate grid size based on board size
        self.pieces = []  # List to hold the pieces

        if initialize:  # Only initialize pieces if the flag is True
            self.initialize_pieces(size)

    def initialize_pieces(self, size):
        """
        Initializes the pieces on the board based on the number of players and board size.

        This function calls either `initialize_2_player_pieces` or `initialize_4_player_pieces`
        depending on the size of the board to set up the initial configuration of pieces.

        Args:
            size (int): The size of the board, used to determine which initialization to perform.
        """
        if size == 8:
            self.initialize_2_player_pieces()
        else:
            self.initialize_4_player_pieces(size)

    def initialize_2_player_pieces(self):
        """
        Initializes pieces for a two-player game.

        Places pieces for Player 1 (black) on the top and bottom rows,
        and Player 2 (white) on the left and right columns.
        """
        for i in range(1, 7):
            self.pieces.append(Piece(0, i, (0, 0, 0)))  # Top row (black)
            self.pieces.append(Piece(7, i, (0, 0, 0)))  # Bottom row (black)
        for i in range(1, 7):
            self.pieces.append(Piece(i, 0, (255, 255, 255)))  # Left column (white)
            self.pieces.append(Piece(i, 7, (255, 255, 255)))  # Right column (white)

    def initialize_4_player_pieces(self, size):
        """
        Initializes pieces for a four-player game.

        Places alternating black and red pieces on the top and bottom rows,
        and alternating white and green pieces on the left and right columns.

        Args:
            size (int): The size of the board.


        """


        empty_spaces = (size - 14) // 2
        for i in range(14):
            col_position = empty_spaces + i
            color = (0, 0, 0) if i % 2 == 0 else (255, 0, 0)  # Black (B) and Red (R)
            self.pieces.append(Piece(0, col_position, color))  # Top row
            self.pieces.append(Piece(size - 1, col_position, color))  # Bottom row
        for i in range(6):
            row_position = empty_spaces + i
            color = (255, 255, 255) if i % 2 == 0 else (0, 255, 0)  # White (W) and Green (G)
            self.pieces.append(Piece(row_position, 0, color))  # Left column
            self.pieces.append(Piece(row_position, size - 1, color))  # Right column

    def draw(self, window, selected_piece=None):
        """
        Draws the game board and pieces on the Pygame window.

        This function draws the grid for the board, places the pieces in their
        current positions, and highlights any selected piece.

        Args:
            window (pygame.Surface): The Pygame window surface to draw on.
            selected_piece (Piece, optional): The currently selected piece to highlight (if any).
        """
        tan_color = (210, 180, 140)
        font = pygame.font.SysFont('Arial', 24)
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.grid_size + self.offset, row * self.grid_size + self.offset,
                                   self.grid_size, self.grid_size)
                pygame.draw.rect(window, tan_color, rect)
                pygame.draw.rect(window, (0, 0, 0), rect, 1)
                piece = self.get_piece(row, col)
                if piece:
                    if piece == selected_piece:
                        self.outline_piece(window, piece)
                    piece.draw(window, self.grid_size, self.offset)
        for col in range(self.cols):
            label = font.render(chr(65 + col), True, (0, 0, 0))
            label_rect = label.get_rect(center=(
            col * self.grid_size + self.offset + self.grid_size // 2, self.rows * self.grid_size + self.offset + 20))
            window.blit(label, label_rect)
        for row in range(self.rows):
            label = font.render(str(self.rows - row), True, (0, 0, 0))
            label_rect = label.get_rect(
                center=(self.offset - 20, row * self.grid_size + self.offset + self.grid_size // 2))
            window.blit(label, label_rect)

    def outline_piece(self, window, piece):
        """
        Draws an outline around a selected piece on the board.

        Highlights the selected piece in a distinct color to indicate selection.

        Args:
            window (pygame.Surface): The Pygame window surface to draw on.
            piece (Piece): The selected piece to outline.
        """
        outline_color = (255, 215, 0)
        outline_rect = pygame.Rect(piece.col * self.grid_size + self.offset, piece.row * self.grid_size + self.offset,
                                   self.grid_size, self.grid_size)
        pygame.draw.rect(window, outline_color, outline_rect, 5)

    def get_piece(self, row, col):
        """
        Retrieves the piece at a specific board location.

        Searches for and returns the piece at the specified row and column
        on the board.

        Args:
            row (int): The row of the desired piece.
            col (int): The column of the desired piece.

        Returns:
            Piece or None: The piece at the specified location, or None if no piece exists there.
        """
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def remove_piece(self, piece):
        """
        Removes a piece from the board.

        Deletes the specified piece from the list of active pieces.

        Args:
            piece (Piece): The piece to remove.
        """
        self.pieces.remove(piece)

    def move_piece(self, piece, row, col):
        """
        Moves a piece to a new location on the board.

        Updates the position of the piece and handles capturing an opponent's piece
        if it exists at the destination.

        Args:
            piece (Piece): The piece to move.
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """
        target_piece = self.get_piece(row, col)
        if target_piece and target_piece.color != piece.color:
            self.remove_piece(target_piece)
        piece.row = row
        piece.col = col

    def is_valid_move(self, piece, row, col):
        """
        Validates whether a move is legal based on the game rules.

        Checks if the move is within bounds, follows movement rules, and is not blocked
        by other pieces.

        Args:
            piece (Piece): The piece attempting the move.
            row (int): The destination row for the piece.
            col (int): The destination column for the piece.

        Returns:
            tuple: A tuple (is_valid, message) where is_valid is a boolean indicating if the move is valid,
                   and message contains an error or success message.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False, "Move is out of bounds."
        if self.get_piece(row, col) and self.get_piece(row, col).color == piece.color:
            return False, "Cannot move to a square occupied by your own piece."
        if piece.row == row:
            distance = abs(col - piece.col)
            line_pieces = self.count_pieces_on_line(piece.row, is_row=True)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif piece.col == col:
            distance = abs(row - piece.row)
            line_pieces = self.count_pieces_on_line(piece.col, is_row=False)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        elif abs(piece.row - row) == abs(piece.col - col):
            distance = abs(row - piece.row)
            line_pieces = self.count_diagonal_pieces(piece.row, piece.col, row, col)
            if not self.is_path_clear(piece.row, piece.col, row, col, piece.color):
                return False, "Path is blocked by an opponent's piece."
        else:
            return False, "Invalid move: Not a straight line or diagonal."
        if distance != line_pieces:
            return False, f"Invalid move distance: Attempted {distance}, but required {line_pieces}."
        return True, ""

    def is_path_clear(self, start_row, start_col, end_row, end_col, color):
        """
        Checks if the path between two positions is clear for a piece to move.

        This function checks if the cells between the starting and ending positions are unoccupied
        by opponent pieces, allowing the piece to move along a straight line or diagonal.

        Args:
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.
            end_row (int): The destination row.
            end_col (int): The destination column.
            color (tuple): The color of the moving piece.

        Returns:
            bool: True if the path is clear, False otherwise.
        """
        d_row = (end_row - start_row) // max(1, abs(end_row - start_row))
        d_col = (end_col - start_col) // max(1, abs(end_col - start_col))
        current_row = start_row + d_row
        current_col = start_col + d_col
        while current_row != end_row or current_col != end_col:
            piece = self.get_piece(current_row, current_col)
            if piece:
                if piece.color != color:
                    return False
            current_row += d_row
            current_col += d_col
        return True

    def count_diagonal_pieces(self, start_row, start_col, end_row, end_col):
        """
        Counts the number of pieces along a diagonal between two points.

        Counts all pieces found along a diagonal path between the start and end positions,
        used to determine valid movement distances.

        Args:
            start_row (int): The starting row of the diagonal.
            start_col (int): The starting column of the diagonal.
            end_row (int): The ending row of the diagonal.
            end_col (int): The ending column of the diagonal.

        Returns:
            int: The number of pieces along the diagonal.
        """
        count = 0
        d_row = 1 if end_row > start_row else -1
        d_col = 1 if end_col > start_col else -1
        row, col = start_row, start_col
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row -= d_row
            col -= d_col
        row, col = start_row + d_row, start_col + d_col
        while row >= 0 and row < self.rows and col >= 0 and col < self.cols:
            if self.get_piece(row, col):
                count += 1
            row += d_row
            col += d_col
        return count

    def count_pieces_on_line(self, index, is_row=True):
        """
        Counts the number of pieces on a row or column line.

        Used to determine if a piece can move based on the number of pieces along
        the row or column it is moving through.

        Args:
            index (int): The index of the row or column to count pieces on.
            is_row (bool): A flag indicating whether to count pieces in a row (True) or a column (False).

        Returns:
            int: The number of pieces on the specified line.
        """
        count = 0
        if is_row:
            for col in range(self.cols):
                if self.get_piece(index, col):
                    count += 1
        else:
            for row in range(self.rows):
                if self.get_piece(row, index):
                    count += 1
        return count

    def get_position_notation(self, row, col):
        """
        Converts a board position into chess-like notation.

        Converts the given row and column into standard board game notation
        with column labels (A-H) and row numbers (1-8).

        Args:
            row (int): The row of the position.
            col (int): The column of the position.

        Returns:
            str: A string representing the position in chess notation.
        """
        column_label = chr(65 + col)
        row_label = str(self.rows - row)
        return f"{column_label}{row_label}"

    def get_remaining_colors(self):
        """
        Retrieves a set of all remaining piece colors on the board.

        Collects all unique colors of pieces that are still on the board.

        Returns:
            set: A set containing the colors of all remaining pieces.
        """
        remaining_colors = set()
        for piece in self.pieces:
            remaining_colors.add(piece.color)
        return remaining_colors

    def check_connected_group(self, color):
        """
        Checks if all pieces of a specified color are connected.

        Verifies if all pieces of a given color form a connected group
        or if only one color remains on the board.

        Args:
            color (tuple): The color of the pieces to check.

        Returns:
            bool: True if all pieces are connected or if only one color remains, False otherwise.
        """
        print(f"Checking connected group for color: {self.get_color_name(color)}")

        remaining_colors = self.get_remaining_colors()
        if len(remaining_colors) == 1:
            print("Only one color remains on the board, automatic winner.")
            return True

        start_row, start_col = -1, -1
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    start_row, start_col = row, col
                    break
            if start_row != -1:
                break

        if start_row == -1:
            print("No starting piece found for this color.")
            return False

        self.dfs(start_row, start_col, color, visited)

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and not visited[row][col]:
                    return False

        print(f"All pieces of color {self.get_color_name(color)} are connected.")
        return True

    def dfs(self, row, col, color, visited):
        """
        Performs Depth First Search (DFS) to check for connected pieces.

        Recursively visits all connected pieces of the same color using DFS.

        Args:
            row (int): The row of the current piece.
            col (int): The column of the current piece.
            color (tuple): The color of the pieces being checked.
            visited (list): A 2D list tracking visited pieces.
        """
        row_nbr = [-1, 1, 0, 0, -1, -1, 1, 1]
        col_nbr = [0, 0, -1, 1, -1, 1, -1, 1]
        visited[row][col] = True
        for k in range(8):
            new_row = row + row_nbr[k]
            new_col = col + col_nbr[k]
            if self.is_safe(new_row, new_col, color, visited):
                self.dfs(new_row, new_col, color, visited)

    def is_safe(self, row, col, color, visited):
        """
        Checks if a piece can be safely visited during DFS.

        Validates if the piece at the specified position matches the target color
        and has not been visited.

        Args:
            row (int): The row of the piece to check.
            col (int): The column of the piece to check.
            color (tuple): The color being checked.
            visited (list): The 2D list of visited pieces.

        Returns:
            bool: True if the piece is safe to visit, False otherwise.
        """
        return (0 <= row < self.rows) and (0 <= col < self.cols) and \
            self.get_piece(row, col) and self.get_piece(row, col).color == color and \
            not visited[row][col]

    def get_color_name(self, color):
        """
        Converts an RGB color tuple to a string representing the color name.

        Translates RGB values into user-friendly color names for display purposes.

        Args:
            color (tuple): The RGB tuple of the color.

        Returns:
            str: A string representing the name of the color.
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

    def clear_board(self):
        """
        Clears all pieces from the board.

        Removes all pieces from the board, resetting the game state.
        """
        self.pieces.clear()

    def set_piece(self, row, col, color):
        """
        Places a piece at a specified location on the board.

        Adds a piece with the specified color to the board at the given row and column.

        Args:
            row (int): The row to place the piece in.
            col (int): The column to place the piece in.
            color (tuple): The color of the piece.
        """
        self.pieces.append(Piece(row, col, color))

    def get_pieces(self, color):
        """
        Returns a list of all pieces of a given color on the board.

        Filters and retrieves all pieces of the specified color.

        Args:
            color (tuple): The color of the pieces to retrieve.

        Returns:
            list: A list of pieces matching the specified color.
        """
        return [piece for piece in self.pieces if piece.color == color]
