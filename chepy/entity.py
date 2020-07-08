class Entity:
    def __init__(self,
                 cord):
        self.cord = cord

        self.attacked = False
        self.attacker = None
        self.pinned = False

    def set_attacked(self, status):
        self.attacked = status

    def is_attacked(self):
        return self.attacked

    def set_pinned(self, status, attacker=None):
        if status:
            self.pinned = status
            self.attacker = attacker
        else:
            self.pinned = status
            self.attacker = None
    
    def is_pinned(self):
        return self.pinned, self.attacker


class Empty(Entity):
    def __init__(self, 
                 cord):
        super().__init__(cord)

    def __str__(self):
        return "⊡"

class Piece(Entity):
    def __init__(self,
                 cord,
                 member,
                 moves):
        super().__init__(cord)
        
        self.member = member
        self.moves = moves

    def get_moves(self):
        return self.moves

    def membership(self):
        return self.member

    def set_cord(self, cord):
        self.cord = cord

    def get_cord(self):
        return self.cord

class Pawn(Piece):
    moves = ((0, 1),)
    attack_moves = ((-1, 1), (1, 1))
    special_move = (0, 2)

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, Pawn.moves)

        self.attack_moves = Pawn.attack_moves

        self.special_move = Pawn.special_move
        self.start_cord = cord
    
    def get_attack_moves(self):
        return self.attack_moves

    def can_special(self):
        return self.start_cord == self.cord

    def get_special_move(self):
        return self.special_move

    def __str__(self):
        return "♟︎" if self.member == "white" else "♙"

class Knight(Piece):
    moves = ((-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1))

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, Knight.moves)

    def __str__(self):
        return "♞" if self.member == "white" else "♘"

class Bishop(Piece):
    moves = ((-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, Bishop.moves)

    def __str__(self):
        return "♝" if self.member == "white" else "♗"

class Rook(Piece):
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, Rook.moves)

        self.moved = False
    
    def did_move(self):
        self.moved = True

    def has_moved(self):
        return self.moved

    def __str__(self):
        return "♜" if self.member == "white" else "♖"

class Queen(Piece):
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, Queen.moves)

    def __str__(self):
        return "♛" if self.member == "white" else "♕"

class King(Piece):
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        super().__init__(cord, member, King.moves)

        self.moved = False
    
    def did_move(self):
        self.moved = True

    def has_moved(self):
        return self.moved

    def __str__(self):
        return "♚" if self.member == "white" else "♔"
        


