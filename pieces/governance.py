from game_items.piece import Piece
from game_items.loc import Loc
from game_items.gamevars import BOARD_SIZE

class Governance(Piece):
    """
    Represents the Governance piece in the BoxShogi game. This piece moves diagonally any number of squares and can
    add orthogonal moves upon promotion.
    """
    promoted_dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)] #Orthogonal directions
    dirs = [(1, -1), (-1, 1), (-1, -1), (1, 1)]  # Diagonal directions

    def __init__(self, name):
        """
        Initialize a Governance piece with its name and possible moves.

        :param name: A string representing the name of the piece ('g' for lower, 'G' for upper).
        """
        super().__init__(name)
        self.moves = None

    def make_moves(self, board, start):
        """
        Generate all possible moves for this piece from a given location on a given board.

        :param board: The game board.
        :param start: The starting Loc of this piece.
        """

        # Resetting or initializing the moves cache
        self.moves = []

        # Generate diagonal moves
        for dx, dy in self.dirs:
            x, y = start.get_x() + dx, start.get_y() + dy
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if self.is_path_clear(board, start, Loc(x, y), (dx, dy)):
                    self.moves.append(Loc(x, y))
                
                else:
                    break
                
                x += dx
                y += dy

        # Generate additional orthogonal moves if the piece is promoted
        if self.promoted:
            for dx, dy in self.promoted_dirs:
                x, y= start.get_x() + dx, start.get_y() + dy
                if board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self)):
                    self.moves.append(Loc(x, y))

    def can_move(self, board, start, end):
        """
        Checks if the piece can move to the specified location, considering both diagonal and orthogonal
        moves upon promotion. It verifies the path is clear of obstructions.
        """
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        
        # Check for diagonal movement
        if abs(dx) == abs(dy):
            direction = (dx, dy)  
        # Check for orthogonal movement if promoted
        elif self.promoted and ((dx == 0 and dy != 0) or (dy == 0 and dx != 0)):
            direction = (dx, dy) 
        else:
            return False  # The move is not allowed
        
        return self.is_path_clear(board, start, end, direction)
    
    def is_path_clear(self, board, start, end, direction):
        """
        Checks if the path from start to end is clear, allowing for a capture at the end position.
        """
        x, y = start.get_x(), start.get_y()
        x += direction[0]
        y += direction[1]

        # Traverse the path
        while (x, y) != (end.get_x(), end.get_y()):
            if not board.is_valid(x, y) or board.is_occupied(x, y):
                return False  # Path is blocked
            x += direction[0]
            y += direction[1]

        # Final position validation: must be within bounds and either unoccupied or capturable
        if not(board.is_valid(x, y) and (not board.is_occupied(x, y) or board.is_capturable(x, y, self))):
            return False
        
        return True  # Path is clear

    def can_be_promoted(self):
        """
        Check if this piece can be promoted.

        :return: Always True for Governance, as it can be promoted.
        """
        return True

    def get_moves(self):
        """
        Get all possible moves generated for this piece.

        :return: A list of Loc instances representing all possible moves.
        """
        return self.moves