from chepy.utils import Board

board = Board()

board.print(show_attacked=True)

# translate a chess coordinate
# to the internal representation
pawn_cord = "c2"
# look at the valid moves
# of the pawn
board(pawn_cord)

# check if queen can move
# (she should not)
queen_cord = "d1"
board(queen_cord)

# move the pawn
move_cord = "c4"
board(pawn_cord, move_cord)

# select the black pawn
pawn_cord = "d7"
board(pawn_cord)

# move the pawn
# (open the king for a check)
move_cord = "d5"
board(pawn_cord, move_cord)

# look at the valid moves of the queen
# (now there should be some)
board(queen_cord)

# move the queen
# and check the black king
move_cord = "a4"
board(queen_cord, move_cord)

board.print()
board.print(squares=board.get_attacked_squares())

# check if the king can move
king_cord = "e8"
board(king_cord)

# check if the queen can move
queen_cord = "d8"
board(queen_cord)

# check if the king can move
bishop_cord = "c8"
board(bishop_cord)

# check if the knight can move
knight_cord = "b8"
board(knight_cord)