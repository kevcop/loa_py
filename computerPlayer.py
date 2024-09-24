import random
from board import Board

# Mapping of index to column notation (A-H)
index_to_col = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D',
    4: 'E', 5: 'F', 6: 'G', 7: 'H'
}

class ComputerPlayer:

    """
    Function Name: __init__
    Purpose: To initialize the computer player with a board and piece color.
    Parameters:
        board (Board), the game board.
        color (tuple), the RGB color of the player's pieces, default is white.
    Return Value: None
    Algorithm:
        1) Set the board and player color.
        2) Initialize lists for possible moves and capture moves.
    Reference: None
    """
    def __init__(self, board, color=(255, 255, 255)):
        self.board = board
        self.color = color
        self.possible_moves = []
        self.capture_moves = []

    """
    Function Name: proper_notation
    Purpose: To convert a position to proper chess-like notation (A1, B2, etc.).
    Parameters:
        position (tuple), a tuple representing the (column, row) on the board.
    Return Value: A string representing the position in chess-like notation.
    Algorithm:
        1) Convert the column index to a letter (A, B, C, etc.).
        2) Convert the row index to a 1-based number.
    Reference: None
    """
    def proper_notation(self, position):
        col, row = position
        column_letter = chr(65 + col)
        row_number = row + 1
        return f"{column_letter}{row_number}"

    """
    Function Name: generate_all_possible_moves
    Purpose: To generate all valid moves and capture moves for the AI player.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Clear any previously stored moves.
        2) Iterate through all pieces on the board and generate valid moves for each.
    Reference: None
    """
    def generate_all_possible_moves(self):
        self.possible_moves.clear()
        self.capture_moves.clear()
        print(f"Generating moves for color: {self.color}")

        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.color:
                    print(f"Found piece at {self.proper_notation((col, row))} with color {piece.color}")
                    self.generate_moves_for_piece(row, col)

        print(f"Total possible moves generated: {len(self.possible_moves)}")
        print(f"Total capture moves generated: {len(self.capture_moves)}")
        self.display_generated_moves()

    """
    Function Name: generate_moves_for_piece
    Purpose: To generate valid moves for a specific piece on the board.
    Parameters:
        start_row (int), the row of the piece.
        start_col (int), the column of the piece.
    Return Value: None
    Algorithm:
        1) Generate horizontal, vertical, and diagonal moves based on game rules.
    Reference: None
    """
    def generate_moves_for_piece(self, start_row, start_col):
        horizontal_moves_required = self.board.count_pieces_on_line(start_row, is_row=True)
        for offset in range(1, horizontal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row, start_col + offset)
            self.add_move_if_valid(start_row, start_col, start_row, start_col - offset)

        vertical_moves_required = self.board.count_pieces_on_line(start_col, is_row=False)
        for offset in range(1, vertical_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col)
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col)

        diagonal_moves_required = self.board.count_diagonal_pieces(start_row, start_col, start_row, start_col)
        for offset in range(1, diagonal_moves_required + 1):
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col + offset)
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col - offset)
            self.add_move_if_valid(start_row, start_col, start_row + offset, start_col - offset)
            self.add_move_if_valid(start_row, start_col, start_row - offset, start_col + offset)

    """
    Function Name: add_move_if_valid
    Purpose: To validate a move and add it to the list of possible or capture moves.
    Parameters:
        start_row (int), the starting row of the piece.
        start_col (int), the starting column of the piece.
        end_row (int), the destination row.
        end_col (int), the destination column.
    Return Value: None
    Algorithm:
        1) Validate the move.
        2) Add valid moves to either the possible or capture moves list.
    Reference: None
    """
    def add_move_if_valid(self, start_row, start_col, end_row, end_col):
        if 0 <= end_row < self.board.rows and 0 <= end_col < self.board.cols:
            is_valid, captures = self.validate_move(start_row, start_col, end_row, end_col)
            if is_valid:
                move_details = {'start': (start_row, start_col), 'end': (end_row, end_col), 'captures': captures}
                if captures:
                    self.capture_moves.append(move_details)
                else:
                    self.possible_moves.append(move_details)
                print(f"Valid move found: {self.proper_notation((start_col, start_row))} to {self.proper_notation((end_col, end_row))}")

    """
    Function Name: validate_move
    Purpose: To check if a move is valid and check for potential captures.
    Parameters:
        start_row (int), the starting row of the piece.
        start_col (int), the starting column of the piece.
        end_row (int), the destination row.
        end_col (int), the destination column.
    Return Value: A tuple (is_valid, captures), where is_valid is True if valid and captures is a list of captured pieces.
    Algorithm:
        1) Check if the move is valid according to the board rules.
        2) Check if any opponent pieces are captured.
    Reference: None
    """
    def validate_move(self, start_row, start_col, end_row, end_col):
        captures = []
        piece = self.board.get_piece(start_row, start_col)
        if not piece or piece.color != self.color:
            return False, captures

        is_valid, message = self.board.is_valid_move(piece, end_row, end_col)
        if is_valid:
            target_piece = self.board.get_piece(end_row, end_col)
            if target_piece and target_piece.color != self.color:
                captures.append((end_row, end_col))
            return True, captures

        return False, captures

    """
    Function Name: select_and_execute_move
    Purpose: To select a move from the list of possible or capture moves and execute it on the board.
    Parameters: None
    Return Value: A tuple (start_row, start_col, end_row, end_col) representing the move, or None if no move was executed.
    Algorithm:
        1) Prioritize capture moves if available, otherwise select a random move.
        2) Execute the selected move and return the details.
    Reference: None
    """
    def select_and_execute_move(self):
        if not self.capture_moves and not self.possible_moves:
            print("No possible moves to select from.")
            return None

        if self.capture_moves:
            selected_move = random.choice(self.capture_moves)
        else:
            selected_move = random.choice(self.possible_moves)

        start = selected_move['start']
        end = selected_move['end']
        start_notation = self.proper_notation((start[1], start[0]))
        end_notation = self.proper_notation((end[1], end[0]))

        piece = self.board.get_piece(start[0], start[1])
        print(f"Selected move: {start_notation} to {end_notation}")

        if piece and self.board.is_valid_move(piece, end[0], end[1])[0]:
            if selected_move['captures']:
                for capture in selected_move['captures']:
                    captured_piece = self.board.get_piece(capture[0], capture[1])
                    if captured_piece:
                        self.board.remove_piece(captured_piece)
                        print(f"Captured piece at {self.proper_notation((capture[1], capture[0]))}")

            self.board.move_piece(piece, end[0], end[1])
            print(f"AI moved from {start_notation} to {end_notation}")

            return start[0], start[1], end[0], end[1]
        else:
            print(f"Failed to execute move: {start_notation} to {end_notation}")
            return None

    """
    Function Name: make_move
    Purpose: To have the AI attempt to make a move.
    Parameters: None
    Return Value: A tuple (start_row, start_col, end_row, end_col) representing the executed move, or None if no move was made.
    Algorithm:
        1) Generate all possible moves.
        2) Select and execute a move.
    Reference: None
    """
    def make_move(self):
        print("AI is attempting to make a move...")
        self.generate_all_possible_moves()
        move = self.select_and_execute_move()

        if move is None:
            print("AI could not find a valid move.")
            return None

        return move

    """
    Function Name: display_generated_moves
    Purpose: To display all the generated moves for debugging purposes.
    Parameters: None
    Return Value: None
    Algorithm:
        1) Print all possible moves and capture moves.
    Reference: None
    """
    def display_generated_moves(self):
        print("Displaying all generated moves:")
        if not self.possible_moves and not self.capture_moves:
            print("No moves were generated.")
            return

        print("\nPossible Moves:")
        for move in self.possible_moves:
            start = self.proper_notation((move['start'][1], move['start'][0]))
            end = self.proper_notation((move['end'][1], move['end'][0]))
            print(f"Move from {start} to {end}")

        print("\nCapture Moves:")
        for move in self.capture_moves:
            start = self.proper_notation((move['start'][1], move['start'][0]))
            end = self.proper_notation((move['end'][1], move['end'][0]))
            print(f"Move from {start} to {end} (Capture)")
