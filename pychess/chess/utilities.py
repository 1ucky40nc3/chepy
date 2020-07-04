from .entities import Empty
from .entities import Piece
from .entities import Pawn
from .entities import Knight
from .entities import Bishop
from .entities import Rook
from .entities import Queen
from .entities import King

class Board:
    def __init__(self):
        self.player = "white"

        self.board = self.init_board()
        self.update_attacked_squares()

        self.status = "ongoing"

    def init_board(self):
        board = []

        board.append([Rook((0, 0), "black"), Knight((1, 0), "black"), Bishop((2, 0), "black"), Queen((3, 0), "black"), King((4, 0), "black"), Bishop((5, 0), "black"), Knight((6, 0), "black"), Rook((7, 0), "black")])
        board.append([Pawn((i, 1), "black") for i in range(8)])

        for i in range(4):
            board.append([Empty((j, i + 2)) for j in range(8)])

        board.append([Pawn((i, 6), "white") for i in range(8)])
        board.append([Rook((0, 7), "white"), Knight((1, 7), "white"), Bishop((2, 7), "white"), Queen((3, 7), "white"), King((4, 7), "white"), Bishop((5, 7), "white"), Knight((6, 7), "white"), Rook((7, 7), "white")])
        
        return board

    def __call__(self, source_cord, target_cord=None):
        if target_cord is None:
            target_cord = source_cord

        source_x, source_y = source_cord
        target_x, target_y = target_cord
        
        source = self.board[source_y][source_x]
        target = self.board[target_y][target_x]

        if isinstance(source, Piece):
            source_moves, target_moves = self.get_piece_moves(
                source, 
                source_cord,
                target,
                target_cord
            )
            if target_cord in source_moves or target_moves:
                if target_moves:
                    x, y = target_moves[0]
                    target.set_cord((x, y))
                    self.board[y][x] = target
                    self.board[target_y][target_x] = Empty((target_x, target_y))

                    x, y = (x - 1, y) if (x - 1, y) in source_moves else (x + 1, y)
                    source.set_cord((x, y))
                    self.board[y][x] = source
                    self.board[source_y][source_x] = Empty((source_x, source_y))
                else:
                    source.set_cord(target_cord)
                    self.board[target_y][target_x] = source
                    self.board[source_y][source_x] = Empty((source_x, source_y))

                self.next_turn()
                self.update_attacked_squares()

                if self.status == "check":
                    moves = self.get_player_moves()
                    if any(moves):
                        self.status = "ongoing"
                    else:
                        self.status = "checkmate"

            if target == source:
                print("Source:", str(source))
                print("Source moves:", source_moves)
            else:
                print("Source:", str(source), "  Target:", str(target))
                print("Source moves:", source_moves, "\nTarget moves:", target_moves)
                print()

            if target_cord == source_cord:
                self.print(squares=source_moves)
        else:
            self.print()

    def get_piece_moves(self, 
                        piece, 
                        piece_cord,
                        target, 
                        target_cord):
        piece_x, piece_y = piece_cord
        target_x, _ = target_cord

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

                square = self.board[y][x]
                if isinstance(square, Piece):
                    if (isinstance(piece, Pawn) or 
                        square.membership() == piece.membership()):
                        break

                    check = False
                    if isinstance(piece, King):
                        self.status = "check"
                        check = True
                        
                    if (not check and
                        (isinstance(piece, Bishop) or
                         isinstance(piece, Rook) or
                         isinstance(piece, Queen))): 
                        tmp_x = x
                        tmp_y = y
                        while bound(tmp_x + dx) and bound(tmp_y + dy):
                            tmp_x += dx
                            tmp_y += dy

                            tmp_square = self.board[tmp_y][tmp_x]
                            if isinstance(tmp_square, Piece):
                                if tmp_square.membership() == piece.membership():
                                    break
                                else:    
                                    if isinstance(tmp_square, King):
                                        square.set_pinned(True, pinner=piece)
                                    else:
                                        break 

                valid_piece_moves.append((x, y))
                loop = False
                
                if (isinstance(piece, Pawn) or
                    isinstance(piece, Knight) or
                    isinstance(piece, King)):
                    break

        if isinstance(piece, Pawn):
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

                    square = self.board[y][x]
                    if isinstance(square, Piece):
                        if square.membership() != piece.membership():
                            valid_piece_moves.append((x, y))

            if piece.can_special():
                dx, dy = piece.get_special_move()
                if piece.membership() == "white":
                    dy = - dy

                valid_piece_moves.append((piece_x + dx, piece_y + dy))
        
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

        if (self.status == "check" and
            isinstance(piece, Piece)):
            if isinstance(piece, King):
                tmp_valid_piece_moves = []
                for move in valid_piece_moves:
                    x, y = move
                    if not self.board[y][x].is_attacked():
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
                        tmp_board = self.board
                        x, y = move

                        self.board[y][x] = piece
                        self.board[y][x] = Empty((piece_x, piece_y))

                        tmp_attacked_squares = self.get_attacked_squares()
                        if king_cord not in tmp_attacked_squares:
                            tmp_valid_piece_moves.append(move)
                        
                        self.board = tmp_board
                
                valid_piece_moves = tmp_valid_piece_moves

        if (self.status != "check" and
            isinstance(piece, King) and
            isinstance(target, Empty)):
            if piece.has_moved():
                empty = True

                step =  1 if target_x - piece_x > 0 else -1
                start = piece_x + 1 if step == 1 else target_x + 1
                stop = 7 if step == 1 else 0
                for x in range(start, stop, step):
                    square = self.board[piece_y][x]
                    if isinstance(square, Piece) or square.is_attacked():
                        empty = False

                if empty:
                    sign = -1 if target_x - piece_x < 0 else 1
                    valid_piece_moves.append((piece_x + sign * 2, piece_y))
                    valid_companion_moves.append((piece_x + -sign, piece_y))

        return valid_piece_moves, valid_companion_moves
    
    def get_player_moves(self, player=None, with_pieces=False):
        if player is None:
            player = self.player
                            
        pieces = self.get_player_pieces(player=player)
        
        moves = []
        for piece in pieces:
            piece_moves = self.get_piece_moves(piece, piece.get_cord(), piece, piece.get_cord())
            for move in piece_moves[0]:
                moves.append(move)
        
            if with_pieces:
                moves.append(piece.get_cord())
        
        return moves

    def get_attacked_squares(self, with_attackers=False):
        enemy_player = "white" if self.player == "black" else "black"
        return self.get_player_moves(player=enemy_player, with_pieces=with_attackers)
    
    def update_attacked_squares(self):
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
        self.player = "white" if self.player == "black" else "black"
    
    def get_player_pieces(self, player=None):
        if player is None:
            player = self.player

        player_pieces = []

        for row in self.board:
            for square in row:
                if isinstance(square, Piece):
                    if square.membership() == player:
                        player_pieces.append(square)
        
        return player_pieces

    def print(self, squares=None):
        if squares is None:
            for row in self.board:
                print(["{}{}".format(str(square), "x" if square.is_attacked() else "") for square in row])
        else:
            for y, row in enumerate(self.board):
                line = []
                for x, square in enumerate(row):
                    if (x, y) in squares:
                        line.append("⛝")
                    else:
                        line.append(str(square))
                print(line)
        print()

class Boundary:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def __call__(self, value):
        return value >= self.min and value < self.max