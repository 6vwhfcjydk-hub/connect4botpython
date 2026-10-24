
import Display
import Outcome
import Action
import Score
import AI
#code to ask player which column he/she wants to paste the code
def ask():
    return input('Select column to add_piece to: select between columns 1-7:')
#codes each player's turn, with safeguards for malformed input, full columns and non existent columns
def turn(player,connect_4_board,possible_placement_of_piece,movelist):
    i=ask()
    if i.lower().startswith('resign'):
        print(f"Player {player} has resigned")
        return 'resigned'
    try:
        i=int(i)
        if i>=1 and i<=7:
            did_action_occur = Action.player_add_piece(player, i, connect_4_board, possible_placement_of_piece)
            if did_action_occur and player=='X':
                movelist.append(i)
                return 'O'
            elif did_action_occur and player=='O':
                movelist.append(i)
                return 'X'
            else:
                print("Column full, try again")
                return player
        else:
            print('Invalid Column')
            return player
    except ValueError:
            print('Enter a number from 1-7')
            return player
#Code sequence to run one game
def one_game(connect_4_board, possible_placement_of_piece, scoreboard,typ):
    movelist=[]
    current='X'

    while Outcome.who_won(connect_4_board) is None:
        Display.display_board(connect_4_board)

        if Outcome.board_full(connect_4_board):
            print('Draw!')
            scoreboard['Player X'] += 0.5
            scoreboard['Player O'] += 0.5
            Score.display_score(scoreboard)
            break
        if typ=='2' and current=='X':
            AI.bot_turn(current,connect_4_board, possible_placement_of_piece,movelist)
            current='O'
            continue
        elif typ=='3' and current=='O':
            #Add in the code for the 2nd player bot here. Should flip current from 'O' to 'X'
            AI.bot_turn(current,connect_4_board, possible_placement_of_piece,movelist)
            current='X'
            continue
        nextplayer=turn(current,connect_4_board,possible_placement_of_piece,movelist)
        if nextplayer=='resigned':
            movelist.append(f"{current} resigned here")
            Score.update_score(Outcome.resigned(current), scoreboard)
            break
        current=nextplayer
    Display.display_board(connect_4_board)
    if Outcome.who_won(connect_4_board) is not None:
        Score.update_score(Outcome.who_won(connect_4_board), scoreboard)
    return movelist