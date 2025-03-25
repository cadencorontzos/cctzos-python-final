import os
from game_items.loc import Loc
from pieces.drive import Drive
from pieces.notes import Notes
from pieces.governance import Governance
from pieces.shield import Shield
from pieces.relay import Relay
from pieces.preview import Preview
from game_items.gamevars import BOARD_SIZE

class Board:
    """
    Class that represents the BoxShogi board
    """
    
    def __init__(self):
        # Initialize an empty 5x5 board
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    def init_pieces(self):
        """
        Initialize the board with pieces in their starting positions.
        """
        # Mapping of starting positions and corresponding pieces
        starting_positions = {
            'a1': Drive("d"), 'e1': Notes("n"), 'd1': Governance("g"),
            'b1': Shield("s"), 'c1': Relay("r"), 'a2': Preview("p"),
            'e5': Drive("D"), 'a5': Notes("N"), 'b5': Governance("G"),
            'd5': Shield("S"), 'c5': Relay("R"), 'e4': Preview("P")
        }

        for loc, piece in starting_positions.items():
            self.set_piece(Loc(loc[0], int(loc[1])), piece)

        
    def _create_piece_from_repr(self, piece_repr):
        """
        Create a piece instance based on its string representation.

        :param piece_repr: The string representation of the piece.
        :return: An instance of the corresponding piece class.
        """
        string_to_piece_class = {
            "d": Drive, "D": Drive, "n": Notes, "N": Notes,
            "g": Governance, "G": Governance, "s": Shield,
            "S": Shield, "r": Relay, "R": Relay, "p": Preview, "P": Preview
        }

        #If piece needs to be promoted
        promoted = piece_repr.startswith("+")

        if promoted:
            piece_repr = piece_repr[1:]

        piece_class = string_to_piece_class.get(piece_repr)

        if piece_class:
            piece = piece_class(piece_repr)
            if promoted:
                piece.promote()
            return piece

        return None
    
    def get_piece(self, x, y):
        """
        Retrieve a piece from the board using x and y coordinates.

        :param x: The x-coordinate (column).
        :param y: The y-coordinate (row).
        :return: The piece at the specified coordinates or None if the square is empty or coordinates are out of bounds.
        """

        if self.is_valid(x, y):
            return self._create_piece_from_repr(self.board[x][y])
        else:
            raise ValueError("Coordinates out of bounds")

    def set_piece(self, loc, piece):
        """
        Place a piece on the board at the specified location.

        :param loc: A Loc object indicating where to place the piece.
        :param piece: The piece to place on the board.
        """
        if self.is_valid_loc(loc):
            self.board[loc.get_x()][loc.get_y()] = str(piece)
        else:
            raise ValueError("Invalid location for placing a piece " + piece + " at location " + loc)
    
    def remove_piece(self, loc):
        """
        Remove a piece from the board at the specified location.

        :param loc: A Loc object indicating where to remove the piece from.
        """
        if self.is_valid_loc(loc):
            self.board[loc.get_x()][loc.get_y()] = ""
        else:
            raise ValueError("Invalid location for removing a piece at location " + loc)
    
    def is_capturable(self, x, y, piece):
        """
        Determines if a piece at a given location can be captured by another piece.

        :param x: The x-coordinate (column) of the location to check on the board.
        :param y: The y-coordinate (row) of the location to check on the board.
        :param piece: The piece attempting to capture the piece at location (x, y). 
        :return: True if the piece at location (x, y) is occupied by an opponent's piece and thus capturable. 
        Returns False if the location is unoccupied, or if the piece at (x, y) belongs to the same player as the 'piece' parameter.
        """
        if self.is_occupied(x, y):
            cur_piece = self.get_piece(x, y)
            if (cur_piece.is_upper() and piece.is_upper()) or (cur_piece.is_lower() and piece.is_lower()):
                return False
            
            else:
                return True
        
        else:
            return False

    def find_drive(self, player):
        """
        Find the Drive piece on the board for a given player.

        :param player: A player object indicating which player's drive to find.
        """
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if player.get_name() == "UPPER":
                    if self.board[x][y] == "D":
                        return Loc(x, y)
                
                if player.get_name() == "lower":
                    if self.board[x][y] == "d":
                        return Loc(x, y)
        return "" 
    
    def is_occupied(self, x, y):
        """
        Check if the specified position is occupied.
        
        :param x: The x-coordinate (column).
        :param y: The y-coordinate (row).
        :return: A boolean indicating if a piece is on the specified point.
        """
        return self.board[x][y] != ""
    
    def is_valid(self, x_board, y_board):
        """
        Check if the specified coordinates are within the board's bounds.
        
        :param x: The x-coordinate (column).
        :param y: The y-coordinate (row).
        :return: A boolean indicating if the point is in bounds.
        """
        return 0 <= x_board < BOARD_SIZE and 0 <= y_board < BOARD_SIZE

    def is_valid_loc(self, loc):
        """
        Check if the position specified by a Loc object is within the board's bounds.
        
        :param loc: A Loc object indicating the location to retrieve the piece from.
        :return: A boolean indicating if the point is in bounds.
        """
        return self.is_valid(loc.get_x(), loc.get_y())

    def __repr__(self):
        return self._stringifyBoard()

    def _stringifyBoard(self):
        """
        Utility function for printing the board

        :return: A string representation of the board.
        """
        s = ''
        for row in range(len(self.board) - 1, -1, -1):

            s += '' + str(row + 1) + ' |'
            for col in range(0, len(self.board[row])):
                s += self._stringifySquare(self.board[col][row])

            s += os.linesep

        s += '    a  b  c  d  e' + os.linesep
        return s

    def _stringifySquare(self, sq):
        """
       	Utility function for stringifying an individual square on the board

        :param sq: Array of strings.
        :return: A string representation of the square.
        """
        if type(sq) is not str or len(sq) > 2:
            raise ValueError('Board must be an array of strings like "", "P", or "+P"')
        if len(sq) == 0:
            return '__|'
        if len(sq) == 1:
            return ' ' + sq + '|'
        if len(sq) == 2:
            return sq + '|'