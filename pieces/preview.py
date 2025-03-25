from game_items.piece import Piece
from game_items.loc import Loc

class Preview(Piece):
    """
    Represents the Preview piece in BoxShogi
    """
    #Directions for lower player if piece is promoted
    lower_promoted_dirs = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (-1, 1)]    
    #Directions for upper player if piece is promoted
    upper_promoted_dirs = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (-1, -1)]

    def __init__(self, name):
        """
        Initializes a Preview piece with its name.
        
        :param name: A string representing the name of the piece ('p' for lower, 'P' for upper).
        """
        super().__init__(name)
        self.moves = []

    def can_move(self, board, start, end):
        """
        Directly checks if the piece can move to the specified end location from its start location.

        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        :param end: The destination of the piece.

        :return: A boolean indicating whether move is legal or not.
        """
        start_x, start_y = start.get_x(), start.get_y()
        end_x, end_y = end.get_x(), end.get_y()
        dx = end_x - start_x
        dy = end_y - start_y

        if not self.is_promoted():
            # For non-promoted pieces, only forward moves are allowed
            forward_direction = -1 if self.is_upper() else 1
            if dx == 0 and dy == forward_direction:
                if board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self)):
                    return True
                
        else:
            # For promoted pieces, check if the move is within the allowed directions
            allowed_directions = self.lower_promoted_dirs if self.is_lower() else self.upper_promoted_dirs
            if (dx, dy) in allowed_directions:
                if board.is_valid(end_x, end_y) and (not board.is_occupied(end_x, end_y) or board.is_capturable(end_x, end_y, self)):
                    return True    
                
        return False

    def make_moves(self, board, start):
        """
        Generates all possible moves for the piece from its current location.
        
        :param board: The current game board.
        :param start: The starting location of the piece as a Loc object.
        """
        self.moves = []
        if not self.promoted:
            # For non-promoted pieces, calculate the forward move based on player
            y_offset = 1 if self.is_lower() else -1
            x, y = start.get_x(), start.get_y() + y_offset
            if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                self.moves.append(Loc(x, y))
        else:
            # For promoted pieces, iterate through possible directions
            locations = self.lower_promoted_dirs if self.is_lower() else self.upper_promoted_dirs
            for dx, dy in locations:
                x, y = start.get_x() + dx, start.get_y() + dy
                if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                    self.moves.append(Loc(x, y))

    def can_be_promoted(self):
        """
        Determines if the piece can be promoted.
        
        :return: Always True, as Preview pieces can be promoted.
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