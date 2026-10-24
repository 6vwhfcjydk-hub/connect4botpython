# Create 4 functions - check if there's 4 in 1 column, 4 in 1 row, 4 in 1 diagonal column down,
# and 4 in 1 diagonal column up.
# Then merge all 4 functions to see if at least 1 condition is fulfilled
def check_horizontal_win(board):
    for row in board:
        for x in range(4):
            if row[x] == row[x + 1] == row[x + 2] == row[x + 3] and row[x] != '.':
                won_player = row[x]
                return won_player
    return False


def check_vertical_win(board):
    for x in range(7):
        for y in range(3):
            if board[y][x] == board[y + 1][x] == board[y + 2][x] == board[y + 3][x] and board[y][x] != '.':
                won_player = board[y][x]
                return won_player
    return False


# Using method of elimination, we can deduce (see picture in document) that only indexes of said
# type can lead to downward connect 4s.
# A loop has been used to create a list of lists that refer to which indexes could possibly
# create downward connect 4s
def diagonal_down_list():
    diagonal_down_list = []
    for x in range(3):
        for y in range(4):
            diagonal_down_list.append([x, y])
    return diagonal_down_list


def check_diagonal_down_win(board):
    down_list = diagonal_down_list()
    for item in down_list:
        if (board[item[0]][item[1]] == board[item[0] + 1][item[1] + 1] ==
                board[item[0] + 2][item[1] + 2] == board[item[0] + 3][item[1] + 3] and
                board[item[0]][item[1]] != '.'):
            won_player = board[item[0]][item[1]]
            return won_player
    return False


# Same story for diagonal up win
def diagonal_up_list():
    diagonal_up_list = []
    for x in range(3, 6):
        for y in range(4):
            diagonal_up_list.append([x, y])
    return diagonal_up_list


def check_diagonal_up_win(board):
    up_list = diagonal_up_list()
    for item in up_list:
        if (board[item[0]][item[1]] == board[item[0] - 1][item[1] + 1] ==
                board[item[0] - 2][item[1] + 2] == board[item[0] - 3][item[1] + 3] and
                board[item[0]][item[1]] != '.'):
            won_player = board[item[0]][item[1]]
            return won_player
    return False
#One more function-detects which player has resigned and updates score accordingly. Called on player who has resigned, returning player who won 
def resigned(player):
    if player=='x' or player=='X':
        return 'Player O'
    elif player=='o' or player=='O':
        return 'Player X'
    else:
        return False 

# Code designed to find out who won by 4 in a row- used to update the score
def who_won(board):
    possible_endings = [check_diagonal_down_win(board), check_diagonal_up_win(board),
                         check_horizontal_win(board), check_vertical_win(board)]
    for ending in possible_endings:
        if ending != False:
            winner = 'Player ' + ending
            return winner
    return None


# Our last function - check if there are no more moves left
def board_full(board):
    for row in board:
        if '.' in row:
            return False
    return True