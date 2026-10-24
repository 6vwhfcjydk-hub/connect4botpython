import Outcome
import Action
import Evaluation
#Choice system for minimax algo
def choose_move(syb,connect_4_board, possible_placement_of_piece, maximising_player=True, depth=8):
    best_move=None
    best_eval=float('-inf')
    #For each move
    for move in possible_placement_of_piece.keys():
        if possible_placement_of_piece[move]>=0:
            #if it's a valid move, add the piece to the new board and new possible_placement_of_piece
            Action.add_piece(syb,move,connect_4_board,possible_placement_of_piece)
            move_eval=minimax(syb,connect_4_board, possible_placement_of_piece,not maximising_player,(depth-1))
            Action.remove_piece(syb,move,connect_4_board,possible_placement_of_piece)
            #find out how good each move is
            if move_eval>best_eval:
                best_eval=move_eval
                best_move=move
    print(f"Current evaluation is {best_eval}")
    return best_move
def bot_turn(player,connect_4_board, possible_placement_of_piece,movelist):
    i=choose_move(player,connect_4_board, possible_placement_of_piece)
    #find the best move
    Action.add_piece(player, i, connect_4_board, possible_placement_of_piece)
    #Add it to the board(remember, this is the 0-6 index version and not the column version)
    movelist.append(i+1)
    #Add 1 to the move, so that it is in the column version and not the 0-6 index version
#minimax algo
def minimax(syb,connect_4_board,possible_placement_of_piece,maximising_player,depth,alpha=float('-inf'),beta=float('+inf')):
    if Outcome.who_won(connect_4_board) is not None:
        if Outcome.who_won(connect_4_board)=='Player ' + syb:
            return 1000+depth
        else:
            return -1000-depth
    #Look for a winner before using evaluation function, as the evaluation function is not designed to detect a winner
    if depth==0:
        return Evaluation.evaluate(connect_4_board,syb)
    if Outcome.board_full(connect_4_board):
        return 0
    #the trick: give very high values to win/loss
    #if the bot is max player
    if maximising_player:
        max_eval=float('-inf')
        #creates the easiest possible placeholder to get replaced
        for move in possible_placement_of_piece.keys():
            if possible_placement_of_piece[move]>=0:
                #x(for each valid move(but rememeber to deepcopy the board and possible_placement_of_piece before adding a piece, so that the original board and possible_placement_of_piece are not changed))
                Action.add_piece(syb,move,connect_4_board,possible_placement_of_piece)
                #add my own piece, score position for me
                eval = minimax(syb,connect_4_board,possible_placement_of_piece,not maximising_player,(depth-1),alpha,beta)
                #evaluate, reducing depth by 1 and reverse the maximising player
                max_eval=max(max_eval,eval)
                #Choose the best evaluation(best position for me )
                Action.remove_piece(syb,move,connect_4_board,possible_placement_of_piece)
                #This time, instead of having to create a new board and new possible_placement_of_piece for each move,
                #I'll use Action's remove_piece function to remove the piece I just added
                #At the next iteration of the loop the board will be back to original and I can just add and evaluate each move without deepcopy.
                if max_eval > alpha:
                    alpha=max_eval
                if alpha >= beta:
                    break
        return max_eval
    #if it's the human
    else:
        min_eval=float('+inf')
        other_player=None
        if syb=='X':
            other_player='O'
        else:
            other_player='X'
        for move in possible_placement_of_piece.keys():
            if possible_placement_of_piece[move]>=0:
                Action.add_piece(other_player,move,connect_4_board,possible_placement_of_piece)
                #Add the enemy piece
                eval = minimax(syb,connect_4_board, possible_placement_of_piece,not maximising_player,(depth-1),alpha,beta)
                #now score poistion for me 
                min_eval=min(min_eval,eval)
                #Choose the worst evaluation(worst position for me)
                Action.remove_piece(other_player,move,connect_4_board,possible_placement_of_piece)
                #now remove the enemy piece so there's no contamination of the board next iteration
                if min_eval < beta:
                    beta=min_eval
                if alpha >= beta:
                    break
        return min_eval