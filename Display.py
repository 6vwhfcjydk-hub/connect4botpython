
#Displays the board. Will be continuously displayed via a while true loop. list index 0 at top, list index 5 at bottom
def display_board(board):
  for row in board:
    print()
    for item in row:
      print(item,end=' ')