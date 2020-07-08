from .entity import Empty
from .entity import Piece
from .entity import Pawn
from .entity import Knight
from .entity import Bishop
from .entity import Rook
from .entity import Queen
from .entity import King

class Board:
    """
    Object oriented representation of a chess board.
    """
    def __init__(self):
        self.status = "ongoing"
        self.player = "white"

        self.board = self.init_board()
        self.update_attacked_squares()

    def init_board(self):
        """
        Initializes an object oriented representation of a chess board.
        The chess board is build with the position 'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
        This is meant simplify the drawing process of the pieces.
        Pay attention to the fact that the coordinates have to be translated.

        Returns:

        board -- a list of rows with the corresponding chess pieces at their starting position
        """
        board = []

        board.append([Rook((0, 0), "black"), Knight((1, 0), "black"), Bishop((2, 0), "black"), Queen((3, 0), "black"), King((4, 0), "black"), Bishop((5, 0), "black"), Knight((6, 0), "black"), Rook((7, 0), "black")])
        board.append([Pawn((i, 1), "black") for i in range(8)])

        for i in range(4):
            board.append([Empty((j, i + 2)) for j in range(8)])

        board.append([Pawn((i, 6), "white") for i in range(8)])
        board.append([Rook((0, 7), "white"), Knight((1, 7), "white"), Bishop((2, 7), "white"), Queen((3, 7), "white"), King((4, 7), "white"), Bishop((5, 7), "white"), Knight((6, 7), "white"), Rook((7, 7), "white")])
        
        return board

    def __call__(self, source_cord, target_cord=None):
        """
        Request current board status and print position.
        Excecute a turn (if target_cord is not None).

        Argument:

        source_cord -- specified coordinate of a piece on the chess board that shall be examined or moved (either internal coordinate or chess representation e.g. '(0, 0)' or "a8")

        Keyword argument:

        target_cord -- specified coordinate of a square on the chess board the source (content of source_cord square) shall be moved to
        """
        if type(source_cord) is str:
            source_cord = self.translate_cord(source_cord)

        # TODO: find stalemate
        if target_cord is None:
            target_cord = source_cord

        if type(target_cord) is str:
            target_cord = self.translate_cord(target_cord)

        source_x, source_y = source_cord
        target_x, target_y = target_cord
        
        source = self.board[source_y][source_x]
        target = self.board[target_y][target_x]

        if isinstance(source, Piece):
            if source.membership() != self.player:
                print("The specified square is not in the current player's possesion!")
                return self.status

            source_moves, companion_moves = self.get_piece_moves(
                source, 
                source_cord)
            if target_cord in source_moves or companion_moves:
                if self.status == "check":
                    moves = self.get_player_moves()
                    if any(moves):
                        self.status = "ongoing"
                    else:
                        self.status = "checkmate"
                        return self.status

                if companion_moves:
                    companion, (x, y) = companion_moves[0]
                    companion_x, companion_y = companion.get_cord()
                    companion.set_cord((x, y))
                    self.board[y][x] = companion
                    self.board[companion_y][companion_x] = Empty((companion_x, companion_y))

                    x, y = (x - 1, y) if (x - 1, y) in source_moves else (x + 1, y)
                    source.set_cord((x, y))
                    self.board[y][x] = source
                    self.board[source_y][source_x] = Empty((source_x, source_y))
                else:
                    source.set_cord(target_cord)
                    self.board[target_y][target_x] = source
                    self.board[source_y][source_x] = Empty((source_x, source_y))
                
                if (isinstance(source, Rook) or
                    isinstance(source, King)):
                    source.did_move()

                self.next_turn()
                self.update_attacked_squares()

            if target == source:
                print("Source:", str(source))
                print("Source moves:", source_moves)
            else:
                print("Source:", str(source), "  Target:", str(target))
                print("Source moves:", source_moves, "\nCompanion moves:", companion_moves)
                print()

            if target_cord == source_cord:
                self.print(squares=source_moves)
            else:
                self.print()
        
        return self.status

    def get_piece_moves(self, 
                        piece, 
                        piece_cord,
                        attacking=False,
                        board=None):
        """
        Find all valid moves of a chess piece.

        Arguments:

        piece -- the piece for which the valid moves shall be computed
        piece_cord -- coordinates of the piece on the board

        Keyword arguments:

        board -- the board which has the position that shall be explored (default None --> the current board)

        Returns:

        valid_piece_moves -- all valid moves for the speciefied piece
        valid_companion_moves -- set of tuples (piece object, list of moves) to specify another piece that has be moved (e.g. castling)
        """
        if board is None:
            board = self.board

        piece_x, piece_y = piece_cord

        moves = piece.get_moves()
        valid_piece_moves = []
        valid_companion_moves = []

        bound = Boundary(0, 8)
        for move in moves:
            dx, dy = move
            if piece.membership() == "white":
                dy = - dy
            
            loop = True
            x = piece_x
            y = piece_y
            while loop and bound(x + dx) and bound(y + dy):
                x += dx
                y += dy

                square = board[y][x]
                if isinstance(square, Piece):
                    if (isinstance(piece, Pawn) or
                        square.membership() == piece.membership()):
                        break

                    if square.membership() != piece.membership():
                        loop = False

                    check = False
                    if isinstance(square, King):
                        self.status = "check"
                        check = True
                        loop = False
    
                    if (not check and
                        (isinstance(piece, Bishop) or
                         isinstance(piece, Rook) or
                         isinstance(piece, Queen))): 
                        tmp_x = x
                        tmp_y = y
                        while bound(tmp_x + dx) and bound(tmp_y + dy):
                            tmp_x += dx
                            tmp_y += dy

                            tmp_square = board[tmp_y][tmp_x]
                            if isinstance(tmp_square, Piece):
                                if tmp_square.membership() == piece.membership():
                                    break
                                else:    
                                    if isinstance(tmp_square, King):
                                        square.set_pinned(True, pinner=piece)
                                    else:
                                        break 

                valid_piece_moves.append((x, y))
                
                if (isinstance(piece, Pawn) or
                    isinstance(piece, Knight) or
                    isinstance(piece, King)):
                    break

        # check if piece is pawn
        # and can execute it's unique movement
        if isinstance(piece, Pawn):
            attacking_moves = []

            moves = piece.get_attack_moves()
            for move in moves:
                dx, dy = move
                if piece.membership() == "white":
                    dy = - dy

                x = piece_x
                y = piece_y
                if bound(x + dx) and bound(y + dy):
                    x += dx
                    y += dy

                    square = board[y][x]
                    if (not attacking and
                        isinstance(square, Piece)):
                        if square.membership() != piece.membership():
                            attacking_moves.append((x, y))

                    elif attacking:
                        if isinstance(square, Piece):
                            if square.membership() != piece.membership():
                                attacking_moves.append((x, y))
                        else:
                            attacking_moves.append((x, y))                        

            if attacking:
                valid_piece_moves = attacking_moves
            else:
                for move in attacking_moves:
                    valid_piece_moves.append(move)

                if piece.can_special():
                    dx, dy = piece.get_special_move()
                    if piece.membership() == "white":
                        dy = - dy

                    valid_piece_moves.append((piece_x + dx, piece_y + dy))
        
        # check if piece is pinned
        # and can move in the direction of the attacker
        pinned, attacker = piece.is_pinned()
        if pinned:
            attacker_x, attacker_y = attacker.get_cord()
            dx = attacker_x - piece_x
            dy = attacker_y - piece_y

            def normalize(x):
                if x > 0:
                    return 1
                elif x < 0:
                     return -1
                return 0

            dx = normalize(dx)
            dy = normalize(dy)

            line_of_attack = []

            start_x = min(attacker_x, piece_x)
            stop_x = max(attacker_x, piece_x)
            bound_x = Boundary(start_x, stop_x)
            
            start_y = min(attacker_y, piece_y)
            stop_y = max(attacker_y, piece_y)
            bound_y = Boundary(start_y, stop_y)

            x = piece_x
            y = piece_y
            while bound_x(x + dx) and bound_y(y + dy):
                x += dx
                y += dy

                line_of_attack.append((x, y))

            tmp_valid_piece_moves = []
            for move in valid_piece_moves:
                if move in line_of_attack:
                    tmp_valid_piece_moves.append(move)

            valid_piece_moves = tmp_valid_piece_moves

        # last turn the enemy player checked the king
        # therefore the player has to save the king
        if (self.status == "check" and
            piece.membership() == self.player and
            isinstance(piece, Piece)):
            if isinstance(piece, King):
                tmp_valid_piece_moves = []
                
                for move in valid_piece_moves:
                    x, y = move
                    if not board[y][x].is_attacked():
                        tmp_valid_piece_moves.append(move)
                
                valid_piece_moves = tmp_valid_piece_moves
            else:
                king = None
                pieces = self.get_player_pieces()
                for piece in pieces:
                    if isinstance(piece, King):
                        king = piece
                        break
                
                king_cord = king.get_cord()

                tmp_valid_piece_moves = []
                attacked_squares = self.get_attacked_squares(with_attackers=True)

                for move in valid_piece_moves:
                    if move in attacked_squares:
                        tmp_board = board
                        x, y = move

                        board[y][x] = piece
                        board[y][x] = Empty((piece_x, piece_y))

                        tmp_attacked_squares = self.get_attacked_squares(board=tmp_board)
                        if king_cord not in tmp_attacked_squares:
                            tmp_valid_piece_moves.append(move)
                         
                        board = tmp_board
                
                valid_piece_moves = tmp_valid_piece_moves

        # check if the player can castle
        if (self.status != "check" and
            isinstance(piece, King)):
            if not piece.has_moved():
                for step in range(-1, 2, 2):
                    companion_x = 0 if step == -1 else 7
                    companion_y = piece_y
                    companion = board[companion_y][companion_x]

                    if (isinstance(companion, Rook) or
                        not companion.has_moved()):

                        empty = True

                        start = 5 if step == 1 else 1
                        stop = 7 if step == 1 else 4
                        for x in range(start, stop, step):
                            square = board[piece_y][x]
                            if isinstance(square, Piece) or square.is_attacked():
                                empty = False

                        if empty:
                            valid_piece_moves.append((piece_x + step * 2, piece_y))                            
                            valid_companion_moves.append((companion, (piece_x + -step, piece_y)))

        return valid_piece_moves, valid_companion_moves
    
    def get_player_moves(self, player=None, board=None, attacking=False, with_pieces=False):
        """
        Find all valid moves of a player's chess pieces.

        Keyword arguments:

        player -- the player whose valid moves shall be found (default None --> the current player)
        board -- the board which has the position that shall be explored (default None --> the current board) 
        with_pieces -- boolean that states if the positions of the players pieces shall be added to the output (default False)

        Returns:

        moves -- all valid moves of a player
        """
        if player is None:
            player = self.player

        if board is None:
            board = self.board
                            
        pieces = self.get_player_pieces(player=player, board=board)
        
        moves = []
        for piece in pieces:
            piece_moves = self.get_piece_moves(
                piece, piece.get_cord(), attacking=attacking)

            for move in piece_moves[0]:
                moves.append(move)
        
            if with_pieces:
                moves.append(piece.get_cord())
        
        return moves

    def get_attacked_squares(self, board=None, with_attackers=False):
        """
        Find all squares of the current enemy player attacks.

        Keyword arguments:

        board -- the board which has the position that shall be explored (default None --> the current board)
        with_attackers -- boolean that states if the positions of the attackers shall be returned additionally

        Returns:

        attacked_squares -- list of the attacked squares
        """
        # TODO: exclude pawn special and normal and exchange for attack move
        if board is None:
            board = self.board

        enemy_player = "white" if self.player == "black" else "black"
        attacked_squares = self.get_player_moves(
            player=enemy_player, 
            board=board,
            attacking=True, 
            with_pieces=with_attackers)

        return attacked_squares
    
    def update_attacked_squares(self):
        """
        Reset the attacked and pinned attributes of the entities to account for the current board position.
        """
        for row in self.board:
            for square in row:
                if square.is_pinned():
                    square.set_attacked(False)
                    square.set_pinned(False)

        attacked_squares = self.get_attacked_squares()
        for square in attacked_squares:
            x, y = square
            self.board[y][x].set_attacked(True)

    def next_turn(self):
        """
        Change the player the indicate the next turn.
        """
        self.player = "white" if self.player == "black" else "black"
    
    def get_player_pieces(self, player=None, board=None):
        """
        Find a player's pieces.

        Keyword arguments:

        player -- the player whose pieces shall be seeked (default None --> the current player)
        board -- the board which has the position that shall be explored (default None --> the current board)

        Returns:

        player_pieces -- list of the pieces of the specified player
        """
        if player is None:
            player = self.player

        if board is None:
            board = self.board

        player_pieces = []

        for row in board:
            for square in row:
                if isinstance(square, Piece):
                    if square.membership() == player:
                        player_pieces.append(square)
        
        return player_pieces
    
    def translate_cord(self, cord):
        """
        Translate a coordinate in chess notation into the internal representation.
        Examples: 'a1' --> (0, 7); 'h8' --> (7, 0)

        Arguments:

        cord -- coordinate in chess notation (lowercase letter [a-h] followed by integer [1-8])

        Returns:

        tuple -- translated (x, y) coordinate
        """
        x = cord[0]
        y = cord[1]

        x = ord(x) - ord("a")
        y = abs(int(y) - 8)

        return x, y

    def print(self, squares=None, show_attacked=False):
        """
        Print the current board.

        Keyword arguments:

        squares -- list of squares on the chess board that shall be marked with this character '⛝' (to indicate that they are attacked)
        show_attacked -- boolean that states if all attacked squares shall be marked
        """

        if squares is None:
            squares = []

        attacked = []
        if show_attacked:
            for y, row in enumerate(self.board):
                for x, square in enumerate(row):
                    if square.is_attacked():
                        attacked.append((x, y))

        for y, row in enumerate(self.board):
            line = []
            for x, square in enumerate(row):
                if (x, y) in squares:
                    line.append("⛝")
                elif (x, y) in attacked:
                    line.append("%")
                else:
                    line.append(str(square))
            print(line)
        print()

class Boundary:
    """
    Class that is used to check if a value is in a boundary.
    """
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def __call__(self, value):
        """
        Check if the value is inside the boundary set at initialization.

        Arguments:

        value -- value that shall be checked

        Returns:

        boolean -- is the value inside the specified boundary?
        """
        return value >= self.min and value < self.max