from game_items.loc import Loc
from game_items.gamevars import BOARD_SIZE

class Player:
    """
    Represents a player in the game, managing their name, captured pieces, and potential moves.
    """

    def __init__(self, name):
        """
        Initializes a new Player with a given name.

        :param name: The name of the player (e.g., "UPPER" or "lower").
        """
        self.name = name
        self.captured = []

    def get_name(self):
        """
        Returns the name of the player.

        :return: The player's name.
        """
        return self.name

    def get_captured(self):
        """
        Returns a list of pieces captured by the player.

        :return: A list of captured pieces.
        """
        return self.captured

    def capture_piece(self, piece):
        """
        Adds a piece to the player's list of captured pieces. 
        Handles promoted pieces by storing their base name.

        :param piece: The piece to be captured.
        """
        if piece.is_promoted():
            self.captured.append(str(piece)[1])
            return
        
        self.captured.append(piece)

    def remove_captured(self, piece):
        """
        Removes a piece from the player's list of captured pieces.

        :param piece_identifier: The identifier of the piece to remove.
        """
        if piece in self.captured:
            self.captured.remove(piece)

    def print_win_message(self, reason):
        """
        Prints a message declaring the player as the winner.

        :param reason: The reason for the win.
        """
        print(f"{self.name} player wins.{reason}")

    def print_captured_list(self):
        """
        Prints a list of the player's captured pieces.
        """
        captured_pieces = " ".join(str(p) for p in self.captured)
        if len(captured_pieces) > 0:
            print(f"Captures {self.name}: {captured_pieces}")
        else:
            print(f"Captures {self.name}: ")

    def piece_in_promote_row(self, loc):
        """
        Checks if a piece is in its promotion row on the board.

        :param loc: The location of the piece.
        :return: True if the piece is in its promotion row, False otherwise.
        """
        
        return (self.name == "UPPER" and loc.get_y() == 0) or (self.name == "lower" and loc.get_y() == 4)


    def captured_piece(self, name):
        """
        Finds a captured piece by its name.

        :param name: The name of the piece to find.
        :return: The piece if found, None otherwise.
        """
        for piece in self.captured:
            if piece.__str__().lower()[0] == name[0]:
                return piece
        return None

    def all_possible_moves(self, board):
        """
        Computes all possible moves for the player's pieces on the board.

        :param board: The game board.
        :return: A list of all possible moves.
        """
        all_moves_list = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = board.get_piece(r, c)
                if piece is None:
                    continue
                if piece.belongs_to(self):
                    piece.make_moves(board, Loc(r, c))
                    all_moves_list.extend(piece.get_moves())  
        return all_moves_list
