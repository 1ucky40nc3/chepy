from chess.utils import Board

board = Board()

# translate a chess coordinate
# to the internal representation
pawn_cord = "c2"
pawn_cord = board.translate_cord(pawn_cord)
pawn_cord

board.print(show_attacked=True)

# look at the valid moves
# of the pawn
board(pawn_cord)

# translate a chess coordinate
# to the internal representation
queen_cord = "d1"
queen_cord = board.translate_cord(queen_cord)
queen_cord

# look at the valid moves
# of the queen
board(queen_cord)

# translate a chess coordinate
# to the internal representation
move_cord = "c4"
move_cord = board.translate_cord(move_cord)
move_cord

# move the pawn
board(pawn_cord, move_cord)

# translate a chess coordinate
# to the internal representation
pawn_cord = "d7"
pawn_cord = board.translate_cord(pawn_cord)
pawn_cord

board(pawn_cord)

# translate a chess coordinate
# to the internal representation
move_cord = "d5"
move_cord = board.translate_cord(move_cord)
move_cord

board(pawn_cord, move_cord)

# look at the valid moves
# of the queen
board(queen_cord)

# translate a chess coordinate
# to the internal representation
move_cord = "a4"
move_cord = board.translate_cord(move_cord)
move_cord

board(queen_cord, move_cord)



