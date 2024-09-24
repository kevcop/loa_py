import pygame
from piece import Piece

class Board:
    """
       Function Name: __init__
       Purpose: To initialize the game board with a given size and optionally place pieces.
       Parameters:
           size (int), an integer that refers to the number of rows and columns.
           initialize (bool), a boolean flag to determine whether pieces should be initialized.
       Return Value: None
       Algorithm:
           1) Set rows, columns, window size, offset, and grid size.
           2) Initialize pieces if the flag is set to True.
       Reference: None
       """
    def __init__(self, size, initialize=True):

        self.rows = size
        self.cols = size
        self.window_size = 800
        self.offset = 50
        self.grid_size = (self.window_size - self.offset * 2) // size
        self.pieces = []

        if initialize:
            self.initialize_pieces(size)


        """
        Function Name: initialize_pieces
        Purpose: To initialize the pieces on the board depending on the number of players.
        Parameters:
            size (int), an integer representing the size of the board.
        Return Value: None
        Algorithm:
            1) Check if the size is 8 and initialize two-player pieces.
            2) Otherwise, initialize four-player pieces.
        Reference: None
        """

    def initialize_pieces(self, size):
        if size == 8:
            self.initialize_2_player_pieces()
        else:
            self.initialize_4_player_pieces(size)

        """
        Function Name: initialize_2_player_pieces
        Purpose: To place pieces for a two-player game.
        Parameters: None
        Return Value: None
        Algorithm:
            1) Place black pieces on the top and bottom rows.
            2) Place white pieces on the left and right columns.
        Reference: None
        """

    def initialize_2_player_pieces(self):
        for i in range(1, 7):
            self.pieces.append(Piece(0, i, (0, 0, 0)))
            self.pieces.append(Piece(7, i, (0, 0, 0)))
        for i in range(1, 7):
            self.pieces.append(Piece(i, 0, (255, 255, 255)))
            self.pieces.append(Piece(i, 7, (255, 255, 255)))

        """
        Function Name: initialize_4_player_pieces
        Purpose: To place pieces for a four-player game based on the board size.
        Parameters:
            size (int), an integer representing the size of the board.
        Return Value: None
        Algorithm:
            1) Place alternating black and red pieces on the top and bottom rows.
            2) Place alternating white and green pieces on the left and right columns.
        Reference: None
        """

    def initialize_4_player_pieces(self, size):

        if size == 12:
            empty_spaces = (size - 10) // 2
            for i in range(10):
                col_position = empty_spaces + i
                color = (0, 0, 0) if i % 2 == 0 else (255, 0, 0)
                self.pieces.append(Piece(0, col_position, color))
                self.pieces.append(Piece(size - 1, col_position, color))
            for i in range(10):
                row_position = empty_spaces + i
                color = (255, 255, 255) if i % 2 == 0 else (0, 255, 0)
                self.pieces.append(Piece(row_position, 0, color))
                self.pieces.append(Piece(row_position, size - 1, color))

        if size == 16:
            empty_spaces = (size - 14) // 2
            for i in range(14):
                col_position = empty_spaces + i
                color = (0, 0, 0) if i % 2 == 0 else (255, 0, 0)
                self.pieces.append(Piece(0, col_position, color))
                self.pieces.append(Piece(size - 1, col_position, color))
            for i in range(14):
                row_position = empty_spaces + i
                color = (255, 255, 255) if i % 2 == 0 else (0, 255, 0)
                self.pieces.append(Piece(row_position, 0, color))
                self.pieces.append(Piece(row_position, size - 1, color))

        """
        Function Name: draw
        Purpose: To draw the board and pieces on the game window.
        Parameters:
            window (pygame.Surface), the window where the game is displayed.
            selected_piece (Piece), an optional piece that is highlighted (default is None).
        Return Value: None
        Algorithm:
            1) Draw the grid and labels.
            2) Draw pieces and outline selected pieces if applicable.
        Reference: None
        """

    def draw(self, window, selected_piece=None):

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
            label_rect = label.get_rect(center=(col * self.grid_size + self.offset + self.grid_size // 2,
                                                self.rows * self.grid_size + self.offset + 20))
            window.blit(label, label_rect)
        for row in range(self.rows):
            label = font.render(str(self.rows - row), True, (0, 0, 0))
            label_rect = label.get_rect(center=(self.offset - 20, row * self.grid_size + self.offset +
                                                self.grid_size // 2))
            window.blit(label, label_rect)

        """
        Function Name: outline_piece
        Purpose: To draw an outline around a selected piece.
        Parameters:
            window (pygame.Surface), the window where the game is displayed.
            piece (Piece), the piece to be outlined.
        Return Value: None
        Algorithm:
            1) Draw a rectangle around the piece to indicate selection.
        Reference: None
        """

    def outline_piece(self, window, piece):

        outline_color = (255, 215, 0)
        outline_rect = pygame.Rect(piece.col * self.grid_size + self.offset, piece.row * self.grid_size + self.offset,
                                   self.grid_size, self.grid_size)
        pygame.draw.rect(window, outline_color, outline_rect, 5)


        """
        Function Name: get_piece
        Purpose: To retrieve a piece at a specific board location.
        Parameters:
            row (int), the row of the piece.
            col (int), the column of the piece.
        Return Value: The piece at the given location, or None if no piece exists.
        Algorithm:
            1) Search through the list of pieces to find one at the given row and column.
        Reference: None
        """
    def get_piece(self, row, col):

        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None


    """
        Function Name: remove_piece
        Purpose: To remove a specified piece from the board.
        Parameters:
            piece (Piece), the piece to be removed.
        Return Value: None
        Algorithm:
            1) Remove the piece from the list of active pieces.
        Reference: None
        """

    def remove_piece(self, piece):

        self.pieces.remove(piece)


        """
        Function Name: move_piece
        Purpose: To move a piece to a new location on the board and handle captures.
        Parameters:
            piece (Piece), the piece to be moved.
            row (int), the destination row.
            col (int), the destination column.
        Return Value: None
        Algorithm:
            1) Check if a piece of a different color is at the destination and capture it.
            2) Update the piece’s row and column to the new position.
        Reference: None
        """
    def move_piece(self, piece, row, col):

        target_piece = self.get_piece(row, col)
        if target_piece and target_piece.color != piece.color:
            self.remove_piece(target_piece)
        piece.row = row
        piece.col = col


        """
        Function Name: is_valid_move
        Purpose: To check if a move is valid according to game rules.
        Parameters:
            piece (Piece), the piece attempting the move.
            row (int), the destination row.
            col (int), the destination column.
        Return Value: A tuple containing a boolean (True if valid) and a message.
        Algorithm:
            1) Check for out-of-bounds or blocked paths.
            2) Ensure the move is along a valid line (horizontal, vertical, or diagonal).
        Reference: None
        """
    def is_valid_move(self, piece, row, col):

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

    """
        Function Name: is_path_clear
        Purpose: To check if the path between two positions is clear of opponent pieces.
        Parameters:
            start_row (int), the starting row of the piece.
            start_col (int), the starting column of the piece.
            end_row (int), the destination row.
            end_col (int), the destination column.
            color (tuple), the color of the moving piece.
        Return Value: True if the path is clear, False otherwise.
        Algorithm:
            1) Check each position between the start and end for opposing pieces.
        Reference: None
        """

    def is_path_clear(self, start_row, start_col, end_row, end_col, color):

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


    """
        Function Name: count_diagonal_pieces
        Purpose: To count the number of pieces along a diagonal path.
        Parameters:
            start_row (int), the starting row of the diagonal.
            start_col (int), the starting column of the diagonal.
            end_row (int), the ending row of the diagonal.
            end_col (int), the ending column of the diagonal.
        Return Value: The number of pieces along the diagonal.
        Algorithm:
            1) Count pieces from the start to the end of the diagonal path.
        Reference: None
        """

    def count_diagonal_pieces(self, start_row, start_col, end_row, end_col):

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


    """
        Function Name: count_pieces_on_line
        Purpose: To count the number of pieces along a row or column.
        Parameters:
            index (int), the index of the row or column to count pieces on.
            is_row (bool), a boolean indicating whether to count on a row (True) or column (False).
        Return Value: The number of pieces on the specified line.
        Algorithm:
            1) Count pieces in the specified row or column.
        Reference: None
        """
    def count_pieces_on_line(self, index, is_row=True):

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


    """
        Function Name: get_position_notation
        Purpose: To convert a board position into standard chess-like notation.
        Parameters:
            row (int), the row of the position.
            col (int), the column of the position.
        Return Value: A string representing the position in chess notation.
        Algorithm:
            1) Convert the row and column into chess-like notation.
        Reference: None
        """
    def get_position_notation(self, row, col):

        column_label = chr(65 + col)
        row_label = str(self.rows - row)
        return f"{column_label}{row_label}"



    """
        Function Name: get_remaining_colors
        Purpose: To retrieve all remaining colors of pieces on the board.
        Parameters: None
        Return Value: A set containing the colors of all remaining pieces.
        Algorithm:
            1) Iterate over the pieces to collect unique colors.
        Reference: None
        """
    def get_remaining_colors(self):

        remaining_colors = set()
        for piece in self.pieces:
            remaining_colors.add(piece.color)
        return remaining_colors


    """
        Function Name: check_connected_group
        Purpose: To check if all pieces of a specified color are connected.
        Parameters:
            color (tuple), the color of the pieces to check.
        Return Value: True if all pieces are connected, False otherwise.
        Algorithm:
            1) Use Depth First Search (DFS) to verify if all pieces of the same color are connected.
        Reference: None
        """
    def check_connected_group(self, color):

        remaining_colors = self.get_remaining_colors()
        if len(remaining_colors) == 1:
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
            return False

        self.dfs(start_row, start_col, color, visited)

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and not visited[row][col]:
                    return False

        return True


    """
        Function Name: dfs
        Purpose: To perform Depth First Search to check for connected pieces.
        Parameters:
            row (int), the row of the current piece.
            col (int), the column of the current piece.
            color (tuple), the color of the pieces being checked.
            visited (list), a 2D list tracking visited pieces.
        Return Value: None
        Algorithm:
            1) Recursively visit all connected pieces of the same color using DFS.
        Reference: None
        """
    def dfs(self, row, col, color, visited):

        row_nbr = [-1, 1, 0, 0, -1, -1, 1, 1]
        col_nbr = [0, 0, -1, 1, -1, 1, -1, 1]
        visited[row][col] = True
        for k in range(8):
            new_row = row + row_nbr[k]
            new_col = col + col_nbr[k]
            if self.is_safe(new_row, new_col, color, visited):
                self.dfs(new_row, new_col, color, visited)


        """
        Function Name: is_safe
        Purpose: To check if a piece can be safely visited during DFS.
        Parameters:
            row (int), the row of the piece.
            col (int), the column of the piece.
            color (tuple), the color being checked.
            visited (list), the 2D list of visited pieces.
        Return Value: True if the piece is safe to visit, False otherwise.
        Algorithm:
            1) Check if the piece matches the color and has not been visited.
        Reference: None
        """

    def is_safe(self, row, col, color, visited):

        return (0 <= row < self.rows) and (0 <= col < self.cols) and \
            self.get_piece(row, col) and self.get_piece(row, col).color == color and \
            not visited[row][col]


    """
        Function Name: get_color_name
        Purpose: To convert an RGB color tuple to a string representing the color name.
        Parameters:
            color (tuple), the RGB tuple of the color.
        Return Value: A string representing the color name.
        Algorithm:
            1) Translate RGB values into user-friendly color names.
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
        Function Name: clear_board
        Purpose: To clear all pieces from the board.
        Parameters: None
        Return Value: None
        Algorithm:
            1) Remove all pieces from the board.
        Reference: None
        """
    def clear_board(self):

        self.pieces.clear()


        """
        Function Name: set_piece
        Purpose: To place a piece at a specified location on the board.
        Parameters:
            row (int), the row to place the piece in.
            col (int), the column to place the piece in.
            color (tuple), the color of the piece.
        Return Value: None
        Algorithm:
            1) Add a new piece to the board with the specified color.
        Reference: None
        """
    def set_piece(self, row, col, color):

        self.pieces.append(Piece(row, col, color))



        """
        Function Name: get_pieces
        Purpose: To retrieve all pieces of a given color on the board.
        Parameters:
            color (tuple), the color of the pieces to retrieve.
        Return Value: A list of pieces matching the specified color.
        Algorithm:
            1) Filter and return all pieces of the specified color.
        Reference: None
        """

    def get_pieces(self, color):

        return [piece for piece in self.pieces if piece.color == color]
