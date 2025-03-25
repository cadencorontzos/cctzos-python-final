from game_items.gamevars import BOARD_SIZE, MOVE_LIMIT
from game_items.loc import Loc
from game_items.board import Board
from pieces.preview import Preview
from game_items.player import Player

class InteractiveGame:
    def __init__(self):
        self.lower = Player("lower")
        self.upper = Player("UPPER")
        self.cur_player = self.lower
        self.last_move = ""
        self.board = Board()
        self.is_game_over = False
        self.moves = 0

    def start_interactive_game(self):
        """
        Starts an interactive game session, allowing players to input moves via the command line.
        """
        self.board.init_pieces()

        while not self.is_game_over:
            if self.moves >= MOVE_LIMIT:
                print("Tie game. Too many moves.")
                self.is_game_over = True
                return

            print(self.board)
            self.upper.print_captured_list()
            self.lower.print_captured_list()
            print()

            self.handle_player_turn()

            self.moves += 1
            self.switch_players()
    
    def handle_player_turn(self):
        """
        Handles actions during a player's turn, including move input, check status, and win conditions.
        """
        if self.is_in_check():
            print(f"{self.cur_player.get_name()} player is in check!")
            if self.handle_checkmate_condition():
                return

        input_move = input(f"{self.cur_player.get_name()}> ").strip()
        if not input_move:
            self.end_game_for_current_player()
            return

        self.last_move = input_move
        print(f"{self.cur_player.get_name()} player action: {self.last_move}")
        self.process_move(input_move)
    
    def process_move(self, input_move):
        """
        Processes a player's move input, performing either a move or a drop action.
        """
        split = input_move.split()
        if len(split) < 3:
            self.end_game_for_current_player()
            return

        if split[0] == "move":
            self.make_move(split)
        elif split[0] == "drop":
            self.drop_move(split)
        else:
            self.end_game_for_current_player()
        
    def end_game_for_current_player(self):
        """Ends the game due to an illegal move by the current player."""
        print(self.board)
        self.upper.print_captured_list()
        self.lower.print_captured_list()
        print()
        other_player = self.get_other_player()
        other_player.print_win_message("  Illegal move.")
        self.is_game_over = True
    
    def handle_checkmate_condition(self):
        """
        Checks for checkmate condition. Returns True if the game ends due to checkmate.
        """
        available_moves = self.create_available_moves()
        for move in available_moves:
            print(move)
        if not available_moves:
            other_player = self.get_other_player()
            other_player.print_win_message("  Checkmate.")
            self.is_game_over = True
            return True
        return False
    def check_illegal_move(self, promote, initial_position, final_position):
        """
        Check if move is illegal based on promotion, start, and end positions.

        :param promote: Boolean indicating where piece should be promoted
        :param initial_position: Loc object indicating start of piece
        :param final_position: Loc object indicating end of piece

        :return Boolean indicating True if move is illegal or False if move is valid
        """

        if initial_position == final_position:
            return True
        
        #Checking if locations and piece are valid
        if (not self.board.is_valid(initial_position.get_x(), initial_position.get_y()) or 
            not self.board.is_valid(final_position.get_x(), final_position.get_y()) or 
            not self.board.is_occupied(initial_position.get_x(), initial_position.get_y())):

            return True
        
        current_piece = self.board.get_piece(initial_position.get_x(), initial_position.get_y())

        if not current_piece.belongs_to(self.cur_player):
            return True
        
        if promote and (not current_piece.can_be_promoted() or current_piece.is_promoted()):
            return True
        
        return False
    
    def make_move(self, split):
        """
        Processes a 'move' command from the input, executing the move if it's valid.

        :param split: A list of strings representing the move command and its parameters.
        """
               
        promote = False
        if len(split) == 4 and split[3] == "promote":
            promote = True
        
        # Converting positions from string to Loc objects
        initial_position = Loc(ord(split[1][0]) - ord('a'), int(split[1][1]) - 1)
        final_position = Loc(ord(split[2][0]) - ord('a'), int(split[2][1]) - 1)

        if self.check_illegal_move(promote, initial_position, final_position):
            self.end_game_for_current_player()
            return

        current_piece = self.board.get_piece(initial_position.get_x(), initial_position.get_y())

        # Check if valid move for this piece type
        if current_piece.can_move(self.board, initial_position, final_position):
            #Check if piece should be promoted
            if promote and ((self.cur_player.piece_in_promote_row(final_position) or
                                self.cur_player.piece_in_promote_row(initial_position)) and
                            current_piece.can_be_promoted() and not current_piece.is_promoted()):
                current_piece.promote()

            elif (self.cur_player.piece_in_promote_row(final_position) and
                    isinstance(current_piece, Preview) and not current_piece.is_promoted()):
                current_piece.promote()  # Force promotion without mentioning promote for Preview
            
            # Case 1: Destination is empty
            if not self.board.is_occupied(final_position.get_x(), final_position.get_y()):
                self.board.remove_piece(initial_position)
                self.board.set_piece(final_position, current_piece)
                # Check if putting piece here results in check - Illegal
                if self.is_in_check():
                    self.board.set_piece(initial_position, current_piece)
                    self.board.remove_piece(final_position)
                    self.end_game_for_current_player()
                    return
            
            #Case 2: Destination is occupied
            else:
                # Check if player's own piece is occupying space.
                end_piece = self.board.get_piece(final_position.get_x(), final_position.get_y())
                if end_piece.belongs_to(self.cur_player):
                    self.end_game_for_current_player()
                    return
                
                # Opponent's piece is occupying space - so capture
                end_piece.depromote()
                end_piece.change_teams()
                self.board.remove_piece(initial_position)
                self.board.set_piece(final_position, current_piece)
                
                # Check if putting piece here results in check - Illegal
                if self.is_in_check():
                    self.board.set_piece(initial_position, current_piece)
                    self.board.set_piece(final_position, end_piece)
                    self.end_game_for_current_player()
                    return
                
                self.cur_player.capture_piece(end_piece)

        else:
            self.end_game_for_current_player()
            return

    def drop_move(self, split):
        """
        Processes a 'drop' command from the input, placing a previously captured piece on the board if the move is valid.

        :param split: A list of strings representing the drop command and its parameters.
        """

        to_drop = self.cur_player.captured_piece(split[1])
        if to_drop is None:
            self.end_game_for_current_player()
            return
        
        # Creating a Loc object from the string input
        loc = Loc(ord(split[2][0]) - ord('a'), int(split[2][1]) - 1)
        
        # Check if the position is valid and not occupied
        if not self.board.is_valid(loc.get_x(), loc.get_y()) or self.board.is_occupied(loc.get_x(), loc.get_y()):
            self.end_game_for_current_player()
            return

        # Special rules for dropping a Preview piece
        if isinstance(to_drop, Preview):
            if self.cur_player.piece_in_promote_row(loc):
                self.end_game_for_current_player()
                return
            
            # Check if dropping would create an illegal position
            for temp_y in [y for y in range(loc.get_y() - 1, -1, -1)] + [y for y in range(loc.get_y() + 1, BOARD_SIZE)]:
                temp = self.board.get_piece(loc.get_x(), temp_y)
                if temp and temp.belongs_to(self.cur_player) and isinstance(temp, Preview) and not temp.is_promoted():
                    self.end_game_for_current_player()
                    return

            # Simulate drop and check for checkmate scenario
            self.board.set_piece(loc, to_drop)
            self.cur_player = self.get_other_player()
            if self.is_in_check() and len(self.create_available_moves()) == 0:
                self.board.remove_piece(loc)
                self.cur_player = self.get_other_player()
                self.end_game_for_current_player()
                return
            self.cur_player = self.get_other_player()

        # If all checks pass, officially drop the piece
        self.board.set_piece(loc, to_drop)
        self.cur_player.remove_captured(to_drop)
    

    def get_all_drive_moves(self, available_moves, all_targets):
        """
        Generates all valid moves for the 'drive' piece that do not result in check, adding them to the available moves.

        :param available_moves: A set to which valid moves will be added.
        :param all_targets: A set of locations that represent all possible moves by the opponent.
        """

        current_drive_loc = self.board.find_drive(self.cur_player)
        drive = self.board.get_piece(current_drive_loc.get_x(), current_drive_loc.get_y())
        drive.make_moves(self.board, current_drive_loc)

        for move in drive.get_moves():
            if move not in all_targets:
                if self.board.is_occupied(move.get_x(), move.get_y()):
                    cur_piece = self.board.get_piece(move.get_x(), move.get_y())
                    if not cur_piece.belongs_to(self.cur_player):
                        self.board.set_piece(move, drive)
                        self.board.remove_piece(current_drive_loc)

                        if not self.is_in_check():
                            str_move = "move " + str(current_drive_loc) + " " + str(move)
                            available_moves.add(str_move)
                            
                        self.board.set_piece(current_drive_loc, drive)
                        self.board.set_piece(move, cur_piece)

                else:  # If position is empty then simulate
                    self.board.set_piece(move, drive)
                    self.board.remove_piece(current_drive_loc)
                    if not self.is_in_check():
                        str_move = "move " + str(current_drive_loc) + " " + str(move)
                        available_moves.add(str_move)
                    self.board.set_piece(current_drive_loc, drive)
                    self.board.remove_piece(move)

    def get_potential_drops(self, available_moves):
        """
        Simulates dropping each of the current player's captured pieces onto the board and 
        adds the move to available moves if it doesn't result in check.

        :param available_moves: A set to which valid drop moves will be added.
        """

        for piece in self.cur_player.get_captured():
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    loc = Loc(i, j)
                    if not self.board.is_occupied(loc.get_x(), loc.get_y()):
                        self.board.set_piece(loc, piece)
                        if not self.is_in_check():
                            c = str(piece).lower()[0]
                            str_move = "drop " + c + " " + str(loc)
                            available_moves.add(str_move)
                        
                        self.board.remove_piece(loc)

    def create_available_moves(self):
        """
        Generates all valid moves for the current player, including piece 
        moves and drops, and checks for check conditions.

        :return: A sorted list of all possible moves that do not result in the player being in check.
        """
        available_moves = set()
        other_player = self.get_other_player()
        all_targets = other_player.all_possible_moves(self.board)
        
        self.get_all_drive_moves(available_moves, all_targets)
        self.get_potential_drops(available_moves)

        for i in range(BOARD_SIZE):  
            for j in range(BOARD_SIZE):
                cur_piece = self.board.get_piece(i, j)
                loc = Loc(i, j) 
                if cur_piece is not None and cur_piece.belongs_to(self.cur_player):
                    cur_piece.make_moves(self.board, loc)
                    moves = cur_piece.get_moves()
                    for move in moves:
                        piece_at_move = self.board.get_piece(move.get_x(), move.get_y())
                        if piece_at_move is not None and not piece_at_move.belongs_to(self.cur_player):
                            self.board.set_piece(move, cur_piece)
                            self.board.remove_piece(loc)

                            if not self.is_in_check():
                                str_move = "move " + str(loc) + " " + str(move)
                                available_moves.add(str_move)

                            self.board.set_piece(loc, cur_piece)
                            self.board.set_piece(move, piece_at_move)

                        if move in all_targets:
                            # Simulate moving the piece and check for check again
                            self.board.set_piece(move, cur_piece)
                            self.board.remove_piece(loc)

                            if not self.is_in_check():
                                str_move = "move " + str(loc) + " " + str(move)
                                available_moves.add(str_move)
                                
                            self.board.set_piece(loc, cur_piece)
                            self.board.remove_piece(move)
        
        return sorted(list(available_moves))
    
    def is_in_check(self):
        """
        Checks if the current player's king is in check.

        :return: True if the king is in check; False otherwise.
        """
        drive_loc = self.board.find_drive(self.cur_player)
        opponent = self.get_other_player()
        all_targets = opponent.all_possible_moves(self.board)
        return drive_loc in all_targets
    
    def get_other_player(self):
        """Return the opponent player."""
        if self.cur_player.get_name() == "UPPER":
            return self.lower
        else:
            return self.upper
    
    def switch_players(self):
        """
        Switches the current player to the other player.
        """
        self.cur_player = self.get_other_player()