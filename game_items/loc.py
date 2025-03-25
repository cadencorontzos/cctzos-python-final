from game_items.gamevars import BOARD_SIZE

class Loc:
    """
    Class to represent a location on the BoxShogi board.
    Supports initialization with (x, y) coordinates and also direct string input like 'a1'.
    """
    def __init__(self, x, y=None):
        """
        Initialize a Loc object with various input formats.
        
        :param x: Column as a index (int), or a combined string format like 'a1'.
        :param y: Row as an index (int), where 1 represents the first row. Not required if x is a combined string.
        """

        self.x_int = None
        self.x_chr = None  # To hold the column as a lowercase letter
        self.y = None

        if isinstance(x, str) and y is not None:
            # Handle column as letter and row as number
            self.x_int = ord(x.lower()) - ord('a')
            self.y = y - 1
        elif isinstance(x, int) and isinstance(y, int):
            # Handle both column and row as numbers
            self.x_int = x
            self.y = y
        else:
            raise ValueError("Illegal input format")

        # Final validation for board boundaries
        if not (0 <= self.x_int < BOARD_SIZE and 0 <= self.y < BOARD_SIZE):
            raise ValueError("Location is out of bounds")

        # Assigning the column letter
        self.x_chr = chr(self.x_int + ord('a'))

    def get_x(self):
        """
        Get the x-coordinate (column) as an integer.

        :return: The x-coordinate as an integer.
        """
        return self.x_int

    def get_y(self):
        """
        Get the y-coordinate (row).

        :return: The y-coordinate as an integer.
        """
        return self.y

    def __eq__(self, other):
        """
        Check equality with another Loc object.

        :param other: Another Loc object to compare with.
        :return: True if both objects represent the same location, False otherwise.
        """
        if not isinstance(other, Loc):
            return False
        
        return self.x_int == other.get_x() and self.y == other.get_y()

    def __str__(self):
        """
        String representation of the Loc object in the format 'a1'.

        :return: String representation of the location.
        """
        return f"{self.x_chr}{self.y + 1}"