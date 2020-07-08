class Entity:
    """
    Parent class to Empty and Piece.
    Everything on a chess board shall have theese attributes.
    """
    def __init__(self,
                 cord):
        """
        Argument:

        cord -- the coordinate of the entity on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        """
        self.cord = cord

        self.attacked = False
        self.attacker = None
        self.pinned = False

    def set_attacked(self, status):
        """Sets the entity's attacked attribute to the specified status."""
        self.attacked = status

    def is_attacked(self):
        """Get the value of the entity's attacked attribute."""
        return self.attacked

    def set_pinned(self, status, attacker=None):
        """
        Set an entity's pinned status.

        Argument:

        status -- value the pinned attribute will be set to

        Keyword Argument:

        attacker -- piece that is attacking the entity (default None --> the attacked attributes is set to False)  
        """
        if status:
            self.pinned = status
            self.attacker = attacker
        else:
            self.pinned = status
            self.attacker = None
    
    def is_pinned(self):
        return self.pinned, self.attacker


class Empty(Entity):
    """
    A class that represents empty squares on a chess board.
    """
    def __init__(self, 
                 cord):
        """
        Argument:

        cord -- the coordinate of the empty square on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        """
        super().__init__(cord)

    def __str__(self):
        """Get the string representation of an empty field (⊡)."""
        return "⊡"

class Piece(Entity):
    """
    A class that represents a non-empty square on the board.
    This means a piece could be a Pawn, Knight, Bishop, Rook, Queen or King.
    """
    def __init__(self,
                 cord,
                 member,
                 moves):
        """
        Arguments:

        cord -- the coordinate of the piece on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the piece is owned by white or black ("white" or "black")
        moves -- all directions the piece could theoretically move to
        """
        super().__init__(cord)
        
        self.member = member
        self.moves = moves

    def get_moves(self):
        """Get all theoretical moves of the piece."""
        return self.moves

    def membership(self):
        """Get the membership attribute of the piece"""
        return self.member

    def set_cord(self, cord):
        """Set the coordinate of the piece."""
        self.cord = cord

    def get_cord(self):
        """Get the coordinate of the piece."""
        return self.cord

class Pawn(Piece):
    """
    Object oriented representation of a pawn.
    """
    moves = ((0, 1),)
    attack_moves = ((-1, 1), (1, 1))
    special_move = (0, 2)

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the pawn on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the pawn is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, Pawn.moves)

        self.attack_moves = Pawn.attack_moves

        self.special_move = Pawn.special_move
        self.start_cord = cord
    
    def get_attack_moves(self):
        """Get all moves a pawn can use to attack entities."""
        return self.attack_moves

    def can_special(self):
        """Get a boolean that states if a pawn moves 2 squares down the board."""
        return self.start_cord == self.cord

    def get_special_move(self):
        """Get a pawns special move."""
        return self.special_move

    def __str__(self):
        """Get the string representation of the pawn."""
        return "♙" if self.member == "white" else "♟︎"

class Knight(Piece):
    """
    Object oriented represenation of a knight.
    """
    moves = ((-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1))

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the knight on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the kight is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, Knight.moves)

    def __str__(self):
        """Get the string representation of the knight."""
        return "♘" if self.member == "white" else "♞"

class Bishop(Piece):
    """
    Object oriented represenation of a bishop.
    """
    moves = ((-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the bishop on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the bishop is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, Bishop.moves)

    def __str__(self):
        """Get the string representation of the bishop."""
        return "♗" if self.member == "white" else "♝"

class Rook(Piece):
    """
    Object oriented represenation of a rook.
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the rook on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the rook is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, Rook.moves)

        self.moved = False
    
    def did_move(self):
        """Set moved attribute of the rook to True."""
        self.moved = True

    def has_moved(self):
        """Get moved attribute of the rook."""
        return self.moved

    def __str__(self):
        """Get the string representation of the rook."""
        return "♖" if self.member == "white" else "♜"

class Queen(Piece):
    """
    Object oriented represenation of a queen.
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the queen on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the queen is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, Queen.moves)

    def __str__(self):
        """Get the string representation of the queen."""
        return "♕" if self.member == "white" else "♛"

class King(Piece):
    """
    Object oriented represenation of a king.
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self,
                 cord,
                 member):
        """
        Arguments:

        cord -- cord -- the coordinate of the king on the chess board (internal representation - see Board.translate_cord() from chepy.utils)
        member -- string that shows that the king is owned by white or black ("white" or "black"
        """
        super().__init__(cord, member, King.moves)

        self.moved = False
    
    def did_move(self):
        """Set moved attribute of the king to True."""
        self.moved = True

    def has_moved(self):
        """Get moved attribute of the rook."""
        return self.moved

    def __str__(self):
        """Get the string representation of the king."""
        return "♔" if self.member == "white" else "♚"
        


