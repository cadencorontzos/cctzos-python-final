from abc import ABC, abstractmethod

class Piece(ABC):
    """
    An abstract base class representing a generic piece in BoxShogi. 
    """
    def __init__(self, name):
        """
        Initialize a Piece with a name

        :param name: The name of the piece, indicating its type and player ('lower' or 'UPPER').
        """
        self.name = name
        self.promoted = False

    def __str__(self):
        return self.name

    def is_lower(self):
        """
        Check if the piece belongs to the 'lower' player.

        :return: True if the piece is 'lower', False otherwise.
        """
        if self.promoted:
            return self.name[1].islower()
        
        else:
            return self.name[0].islower()

    def is_upper(self):
        """
        Check if the piece belongs to the 'UPPER' player.

        :return: True if the piece is 'UPPER', False otherwise.
        """
        if self.promoted:
            return self.name[1].isupper()
        
        else:
            return self.name[0].isupper()

    def is_promoted(self):
        """
        Check if the piece is promoted.

        :return: True if the piece is promoted, False otherwise.
        """
        return self.promoted

    def promote(self):
        """
        Promote the piece, modifying its name to reflect its promoted status.
        """
        if not self.promoted:
            self.promoted = True
            self.name = "+" + self.name

    @abstractmethod
    def can_move(self, board, start, end):
        """
        Abstract method to determine if the piece can move to a specified location.

        :param board: The current game board.
        :param start: The starting location of the piece.
        :param end: The target location for the move.
        :return: True if the move is valid, False otherwise.
        """
        pass

    @abstractmethod
    def can_be_promoted(self):
        """
        Abstract method to check if the piece can be promoted.

        :return: True if the piece can be promoted, False otherwise.
        """
        pass

    @abstractmethod
    def get_moves(self):
        """
        Abstract method to get all possible moves for the piece.

        :return: A list of all possible moves.
        """
        pass

    @abstractmethod
    def make_moves(self, board, start):
        """
        Abstract method to generate all possible moves from a given location.

        :param board: The current game board.
        :param start: The starting location of the piece.
        """
        pass

    def belongs_to(self, player):
        """
        Check if the piece belongs to a specified player.

        :param player: The player to check against.
        :return: True if the piece belongs to the player, False otherwise.
        """
        if player.get_name() == "UPPER" and self.is_upper():
            return True
        elif player.get_name().lower() == "lower" and self.is_lower():
            return True
        return False

    def change_teams(self):
        """
        Change the owner of the piece, switching it from 'lower' to 'UPPER' or vice versa.
        """
        if self.is_lower():
            self.name = self.name.upper()
        else:
            self.name = self.name.lower()

    def depromote(self):
        """
        Depromote the piece, removing the promotion indicator from its name.
        """
        if self.promoted:
            self.promoted = False
            self.name = self.name[1:]
