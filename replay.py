import Action
import Outcome
import Display
import Initialisation

def replay_turn(player,connect_4_board,possible_placement_of_piece,i):
    Action.player_add_piece(player, i, connect_4_board, possible_placement_of_piece)
    if player=='X':
        return 'O'
    elif player=='O':
        return 'X'
#Code sequence to run one game
def replay_game(movelist):
    connect_4_board, possible_placement_of_piece = Initialisation.initialisation()
    current='X'
    resignation=None
    for move in movelist:
        if isinstance(move,str):
            resignation=move
            break
        Display.display_board(connect_4_board)
        print()
        current=replay_turn(current,connect_4_board,possible_placement_of_piece,move)
    Display.display_board(connect_4_board)
    if Outcome.who_won(connect_4_board) is not None:
        winner = 'Player ' + Outcome.who_won(connect_4_board)
        print(f"{winner} won this match")
    elif resignation is not None:
        print()
        print(resignation)
    elif Outcome.board_full(connect_4_board):
        print()
        print('Drawn match')
    else:
        return None