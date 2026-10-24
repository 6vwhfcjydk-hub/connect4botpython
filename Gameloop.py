#Gameloop that ties in scoreboard and game
import Initialisation
import Display
import Game
import Score
import Notation

def play_game_and_new_game(scoreboard,typ,counter=1,movedict=None):
  if movedict is None:
    movedict=Notation.notate()
  connect_4_board, possible_placement_of_piece = Initialisation.initialisation()
  movelist=Game.one_game(connect_4_board, possible_placement_of_piece, scoreboard,typ)
  movedict[counter]=movelist
  Start_new_game = input('Do you want to play again? y/n')
  if Start_new_game.startswith('y') or Start_new_game.startswith('Y'):
    counter += 1
    Display.display_board(connect_4_board)
    return play_game_and_new_game(scoreboard,typ,counter,movedict)
  else:
    Score.display_score(scoreboard)
    if scoreboard['Player X']==scoreboard['Player O']:
      print('Drawn match!')
    elif scoreboard['Player X']>scoreboard['Player O']:
      print('Player X has won!')
    else:
      print('Player O has won!')
    return movedict