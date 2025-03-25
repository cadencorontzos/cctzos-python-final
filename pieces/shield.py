from game_items.piece import Piece
from game_items.loc import Loc

class Shield(Piece):
    """
    Represents the Shield piece in BoxShogi
    """
    lower_dirs = [(0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    upper_dirs = [(1, -1), (0, -1), (-1, -1), (1, 0), (-1, 0), (0, 1)]

    def __init__(self, name):
        """
        Initialize a Shield piece with a name indicating its allegiance.

        :param name: The name of the piece ('s' for lower, 'S' for upper).
        """
        super().__init__(name)
        self.moves = []

    def can_move(self, board, start, end):
        """
        Determine if the piece can move to a specified location from its current location.

        :param board: The game board.
        :param start: The starting location of the piece as a Loc object.
        :param end: The target location for the piece as a Loc object.
        :return: True if the piece can move to the target location, False otherwise.
        """

        start_x, start_y = start.get_x(), start.get_y()
        end_x, end_y = end.get_x(), end.get_y()
        dx = end_x - start_x
        dy = end_y - start_y

        # Determine the current movement directions based on the allegiance
        current_dirs = self.lower_dirs if self.is_lower() else self.upper_dirs

        # Check if the move is within the allowed movement directions
        if (dx, dy) in current_dirs:
            # Ensure the end position is within the board bounds and either unoccupied or occupied by an opponent's piece
            if not board.is_occupied(end.get_x(), end.get_y()) or board.get_piece(end.get_x(), end.get_y()).is_lower() != self.is_lower():
                return True
        return False

    def make_moves(self, board, start):
        """
        Generate all possible moves for this piece from its current location.

        :param board: The game board.
        :param start: The starting location of the piece as a Loc object.
        """
        self.moves = [] 
        directions = self.lower_dirs if self.is_lower() else self.upper_dirs
        
        for dx, dy in directions:
            x, y = start.get_x() + dx, start.get_y() + dy
            if board.is_valid(x, y):
                # Add the move if the destination is valid (unoccupied or occupied by an opponent's piece)
                if not board.is_occupied(x, y) or board.get_piece(x, y).is_lower() != self.is_lower():
                    self.moves.append(Loc(x, y))

    def get_moves(self):
        """
        Get all generated moves for this piece.

        :return: A list of Loc objects representing all possible moves.
        """
        return self.moves

    def can_be_promoted(self):
        """
        Determine if this piece type can be promoted.

        :return: False, indicating that Shield pieces cannot be promoted.
        """
        return False

    def __str__(self):
        """
        Return a string representation of the piece.

        :return: The name of the piece.
        """
        return self.name    
