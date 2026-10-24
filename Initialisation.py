# Creating the connect 4 board - row index 0 (row 6) shall be the topmost row,
# while row index 5 (row 1) shall be the bottommost row
def create_board():
    connect_4_1_row = ['.', '.', '.', '.', '.', '.', '.']
    connect_4_board = []
    for x in range(6):
        connect_4_board.append(connect_4_1_row[:])
    return connect_4_board


# Creating a possible dictionary of places a player can add his piece to.
# key = column index for connect_4_board, value = the row a new piece would land on;
# once it hits -1, no more pieces can be added to that column
def create_possible_placement_of_piece():
    possible_placement_of_piece = {}
    for x in range(7):
        possible_placement_of_piece[x] = 5
    return possible_placement_of_piece


def initialisation():
    connect_4_board = create_board()
    possible_placement_of_piece = create_possible_placement_of_piece()
    return connect_4_board, possible_placement_of_piece