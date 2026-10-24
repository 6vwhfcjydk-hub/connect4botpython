#Ok, the first row from the bottom (index 5) shall be the bottom row. We'll now create a way for players to add pieces to the board.
#Player 1 will be X, Player 2 will be O. A nested function shall be used, with the outer function defining the player,
#and the inner function placing the piece on the board
#i, the list column, will accept numbers 1-7
def player_add_piece(player,i,board,possible_placement_of_piece):
  if i<1 or i>7:
    print('Invalid column')
  elif player=='X' or player=='x':
    i-=1
    return add_piece('X',i,board,possible_placement_of_piece)
  elif player=='O' or player=='o':
    i-=1
    return add_piece('O',i,board,possible_placement_of_piece)
  else:
    print('Invalid player')
#Ok, the inner function-the hard part. First look inside the dictionary - key would be the column .
#Use the key to retieve the appropriate value.
#However, if the value is -1, then it means no more pieces can be added on that column-print column is full
#Then, use this format: connect_4_board[y][x]=piece, where y, the height of the piece, shall be the value, and x shall be the column
#Then, subtract the value by 1
def add_piece(syb,i,board,possible_placement_of_piece):
  if possible_placement_of_piece[i]<=-1:
    return False
  else:
    row_piece_added_to=possible_placement_of_piece[i]
    board[row_piece_added_to][i]=syb
    possible_placement_of_piece[i]-=1
    return True
# if board is empty and possible_placement_of_piece is at default(keys 1-7, all values at 5(being the bottom row))
# And I add_piece('X',3,board,possible_placement_of_piece), row_piece_added_to=5, board[5][3]='X', possible_placement_of_piece[3]=4.
# Using remove_piece(syb,i,board,possible_placement_of_piece) would mean that the row the piece was removed from would be 4+1=5, and board[5][3]='.', possible_placement_of_piece[3]=5
# if statement designed to catch if column is empty-the value of possible_placement_of_piece should not drop below 5 because row 5 is already the lowest row
def remove_piece(syb,i,board,possible_placement_of_piece):
  if possible_placement_of_piece[i]>=5:
    return False
  else:
    row_piece_removed_from=possible_placement_of_piece[i]+1
    board[row_piece_removed_from][i]='.'
    possible_placement_of_piece[i]+=1
    return True