from game_items.piece import Piece
from game_items.loc import Loc
from game_items.gamevars import BOARD_SIZE

class Notes(Piece):
    """
    Represents the Notes piece in BoxShogi, moving horizontally and vertically across the board.
    Upon promotion, it gains the ability to move diagonally one square in any direction.
    """
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions for horizontal and vertical movement
    promoted_dirs = [(-1, -1), (1, -1), (1, 1), (-1, 1)]  # Diagonal directions for promoted pieces

    def __init__(self, name):
        """
        Initialize a Notes piece with its name.
        
        :param name: The name of the piece ('n' for lower, 'N' for upper).
        """
        super().__init__(name)
        self.moves = []

    def can_move(self, board, start, end):
        """
        Determines if the piece can move to a specified location from its current location.
        
        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        :param end: The targeted location of the piece as a Loc object.
        :return: True if the piece can move to the target location, False otherwise.
        """
        start_x, start_y = start.get_x(), start.get_y()
        end_x, end_y = end.get_x(), end.get_y()
        dx = end_x - start_x
        dy = end_y - start_y

        # Check for basic horizontal or vertical movement
        if dx == 0 or dy == 0:  # Horizontal or vertical move
            if abs(dx) > 1 or abs(dy) > 1:  # Moves more than one square
                direction = (dx, dy)  # Normalize direction for more than one step
                return self.is_path_clear(board, start, end, direction)
            # Single step horizontal or vertical move
            return board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self))

        # Additional diagonal move for promoted pieces
        if self.promoted and abs(dx) == 1 and abs(dy) == 1:
            return board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self))

        return False

    def make_moves(self, board, start):
        """
        Generates all possible moves for the piece from its current location.
        
        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        """
        self.moves = []

        # Generate moves for the basic directions
        for dx, dy in self.dirs:
            self._generate_line_moves(board, start, (dx, dy))

        # Generate moves for promoted piece
        if self.promoted:
            for dx, dy in self.promoted_dirs:
                x, y= start.get_x() + dx, start.get_y() + dy
                if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                    self.moves.append(Loc(x, y))
    
    def _generate_line_moves(self, board, start, direction):
        """
        Helper method to generate linear moves in a specified direction.
        
        :param board: The current game board.
        :param start: The starting location of the piece.
        :param dx: Change in x-direction.
        :param dy: Change in y-direction.
        """
        dx, dy = direction[0], direction[1]
        x, y = start.get_x() + dx, start.get_y() + dy  # Start checking from the next square in the given direction
        
        # Iterate over the board within the movement direction until an obstacle is encountered or the edge of the board is reached
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if board.is_valid(x, y):
                if board.is_occupied(x, y):
                    # Check if it's an opponent's piece, if so, add the move and stop further checks in this direction
                    if board.is_capturable(x, y, self):
                        self.moves.append(Loc(x, y))
                    break  # Stop on the first piece encountered (whether it's capturable or not)
                else:
                    # If the square is not occupied, add the move
                    self.moves.append(Loc(x, y))
            else:
                break  # If the square is not valid (out of bounds), stop checking further
            
            x += dx
            y += dy
        
    def is_path_clear(self, board, start, end, direction):
        """
        Checks if the path from start to end is clear of any pieces, allowing for a capture at the end position.
        """
        x, y = start.get_x() + direction[0], start.get_y() + direction[1]
        end_x, end_y = end.get_x(), end.get_y()
        while (x, y) != (end_x, end_y):
            if not board.is_valid(x, y) or board.is_occupied(x, y):
                return False  # Path is blocked
            x += direction[0]
            y += direction[1]
        # Check the final position
        return board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self))

    def can_be_promoted(self):
        """
        Determines if the piece can be promoted.
        
        :return: Always True, as Notes pieces can be promoted.
        """
        return True

    def get_moves(self):
        """
        Returns a list of all possible moves for the piece.
        
        :return: A list of Loc objects representing possible moves.
        """
        return self.moves

    def __str__(self):
        """
        Returns a string representation of the piece.
        
        :return: The name of the piece.
        """
        return self.name
    