from game_items.piece import Piece
from game_items.loc import Loc

class Relay(Piece):
    """
    Represents the Relay piece in BoxShogi
    """

    def __init__(self, name):
        """
        Initialize a Relay piece with its name.
        
        :param name: A string representing the name of the piece ('r' for lower, 'R' for upper).
        """
        super().__init__(name)
        self.moves = []

    def can_move(self, board, start, end):
        """
        Checks if the piece can move to the specified end location from its start location.
        This includes verifying if the path to the end location is valid based on the piece's
        current movement capabilities and promotion status.
        
        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        :param end: The targeted location of the piece as a Loc object.
        :return: True if the piece can move to the target location, False otherwise.
        """
        start_x, start_y = start.get_x(), start.get_y()
        end_x, end_y = end.get_x(), end.get_y()
        dx = end_x - start_x
        dy = end_y - start_y

        current_dirs = self.get_dirs()

        # Check if the move is within the allowed movement directions
        if (dx, dy) in current_dirs:
            if board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self)):
                return True
        return False

    def make_moves(self, board, start):
        """
        Generates all valid moves from the piece's current location, considering its movement rules
        and whether it is promoted.
        
        :param board: The game board.
        :param start: The current location of the piece as a Loc object.
        """
        self.moves = []
        for dx, dy in self.get_dirs():
            x, y = start.get_x() + dx, start.get_y() + dy
            if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                self.moves.append(Loc(x, y))

    def get_dirs(self):
        """
        Determines the current valid movement directions for the piece.
        
        :return: A list of tuples representing the valid movement directions.
        """
        non_promoted_dirs = [(-1, -1), (1, -1), (1, 1), (0, 1), (-1, 1)] if self.is_lower() else \
                            [(1, -1), (1, 1), (0, -1), (-1, 1), (-1, -1)]
        promoted_dirs = [(0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)] if self.is_lower() else \
                        [(1, -1), (0, -1), (-1, -1), (1, 0), (-1, 0), (0, 1)]
                        
        return promoted_dirs if self.promoted else non_promoted_dirs

    def can_be_promoted(self):
        """
        Checks if the piece can be promoted. Relay pieces can be promoted.
        
        :return: True, indicating that Relay pieces can be promoted.
        """
        return True

    def get_moves(self):
        """
        Retrieves all generated valid moves for the piece.
        
        :return: A list of Loc objects representing all valid moves.
        """
        return self.moves
    
    def __str__(self):
        """
        Provides a string representation of the Relay piece.
        
        :return: The name of the piece.
        """
        return self.name
