from game_items.piece import Piece
from game_items.loc import Loc

class Drive(Piece):
    """
    Represents the Drive piece in BoxShogi, moving one square in any direction.
    This piece cannot be promoted.
    """


    
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    def __init__(self, name):
        """
        Initializes a Drive piece with its name.

        :param name: A string representing the name of the piece ('d' for lower, 'D' for upper).
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
        # Calculate the change in position
        start_x, start_y = start.get_x(), start.get_y()
        end_x, end_y = end.get_x(), end.get_y()
        dx = end_x - start_x
        dy = end_y - start_y

        # Check if the move is within the allowed movement directions
        if (dx, dy) in self.dirs:
            # Ensure the end position is within the board bounds and either unoccupied or occupied by an opponent's piece
            if board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self)):
                return True
        return False

    def make_moves(self, board, start):
        """
        Generates all possible moves for the piece from its current location.

        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        """

        self.moves = []  # Clear any existing moves before generating new ones
        for dx, dy in self.dirs:  # Iterate through all possible directions
            x, y = start.get_x() + dx, start.get_y() + dy
            # Add the move if the square is unoccupied or occupied by an opponent's piece
            if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                    self.moves.append(Loc(x, y))
        
    def can_be_promoted(self):
        """
        Determines if the piece can be promoted.

        :return: False, as Drive pieces cannot be promoted.
        """
        return False

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
