import Outcome
#evaluative algo. 0.05 will be the weight for centrality and 0.25 will be the weightage for connecting 2 pieces in a row and 0.7 will be the weightage of connecting 3 pieces in a row
def evaluate(connect_4_board,syb):
    no_of_x_on_columns_3_5,no_of_o_on_columns_3_5=centrality(connect_4_board)
    no_of_x_3_connected,no_of_o_3_connected=con3(connect_4_board)
    if syb=='X':
        evaluation=((no_of_x_on_columns_3_5-no_of_o_on_columns_3_5)*0.15)+((no_of_x_3_connected-no_of_o_3_connected)*0.85)
        return evaluation
    else:
        evaluation=((no_of_o_on_columns_3_5-no_of_x_on_columns_3_5)*0.15)+((no_of_o_3_connected-no_of_x_3_connected)*0.85)
        return evaluation
def centrality(connect_4_board):
    #returns the number of columns 3-5 of the connect 4 board (indexes 2-4), for both X and O pieces in that order
    no_of_x_on_columns_3_5=0
    no_of_o_on_columns_3_5=0
    for counter in range(2,5):
        for row in connect_4_board:
            if row[counter]=='X':
                if counter==3:
                    no_of_x_on_columns_3_5+=1
                else:
                    no_of_x_on_columns_3_5+=0.75
            elif row[counter]=='O':
                if counter==3:
                    no_of_o_on_columns_3_5+=1
                else:
                    no_of_o_on_columns_3_5+=0.75
    return no_of_x_on_columns_3_5,no_of_o_on_columns_3_5



def con3(connect_4_board):
    no_of_x_3_connected=0
    no_of_o_3_connected=0
    for row in connect_4_board:
        for counter in range(5):
            if row[counter]=='X' and row[counter+1]=='X' and row[counter+2]=='X':
                if counter==0 or counter==4:
                    no_of_x_3_connected+=1
                elif (row[counter-1]=='.' or row[counter+3]=='.'):
                    no_of_x_3_connected+=1
            elif row[counter]=='O' and row[counter+1]=='O' and row[counter+2]=='O':
                if counter==0 or counter==4:
                    no_of_o_3_connected+=1
                elif (row[counter-1]=='.' or row[counter+3]=='.'):
                    no_of_o_3_connected+=1
        for counter in range(4):
            if row[counter]=='X' and ((row[counter+1]=='X' and row[counter+2]=='.') or (row[counter+1]=='.' and row[counter+2]=='X')) and row[counter+3]=='X':
                no_of_x_3_connected+=1
            elif row[counter]=='O' and ((row[counter+1]=='O' and row[counter+2]=='.') or (row[counter+1]=='.' and row[counter+2]=='O')) and row[counter+3]=='O':
                no_of_o_3_connected+=1
    for counter in range(7):
        for row in range(3):
            if connect_4_board[row][counter]=='X' and connect_4_board[row+1][counter]=='X' and connect_4_board[row+2][counter]=='X' and connect_4_board[row+3][counter]=='.':
                no_of_x_3_connected+=1
            elif connect_4_board[row][counter]=='O' and connect_4_board[row+1][counter]=='O' and connect_4_board[row+2][counter]=='O' and connect_4_board[row+3][counter]=='.':
                no_of_o_3_connected+=1
    for item in Outcome.diagonal_down_list():
        if (connect_4_board[item[0]][item[1]]=='X' and connect_4_board[item[0]+1][item[1]+1]=='X' and connect_4_board[item[0]+2][item[1]+2]=='X'):
            no_of_x_3_connected+=1
        elif (connect_4_board[item[0]][item[1]]=='X' and ((connect_4_board[item[0]+1][item[1]+1]=='X' and connect_4_board[item[0]+2][item[1]+2]=='.') or (connect_4_board[item[0]+1][item[1]+1]=='.' and connect_4_board[item[0]+2][item[1]+2]=='X')) and connect_4_board[item[0]+3][item[1]+3]=='X'):
            no_of_x_3_connected+=0.75
        elif (connect_4_board[item[0]][item[1]]=='O' and connect_4_board[item[0]+1][item[1]+1]=='O' and connect_4_board[item[0]+2][item[1]+2]=='O'):
            no_of_o_3_connected+=1
        elif (connect_4_board[item[0]][item[1]]=='O' and ((connect_4_board[item[0]+1][item[1]+1]=='O' and connect_4_board[item[0]+2][item[1]+2]=='.') or (connect_4_board[item[0]+1][item[1]+1]=='.' and connect_4_board[item[0]+2][item[1]+2]=='O')) and connect_4_board[item[0]+3][item[1]+3]=='O'):
            no_of_o_3_connected+=0.75
    for item in Outcome.diagonal_up_list():
        if (connect_4_board[item[0]][item[1]]=='X' and connect_4_board[item[0]-1][item[1]+1]=='X' and connect_4_board[item[0]-2][item[1]+2]=='X'):
            no_of_x_3_connected+=1
        elif (connect_4_board[item[0]][item[1]]=='X' and ((connect_4_board[item[0]-1][item[1]+1]=='X' and connect_4_board[item[0]-2][item[1]+2]=='.') or (connect_4_board[item[0]-1][item[1]+1]=='.' and connect_4_board[item[0]-2][item[1]+2]=='X')) and connect_4_board[item[0]-3][item[1]+3]=='X'):
            no_of_x_3_connected+=0.75
        elif (connect_4_board[item[0]][item[1]]=='O' and connect_4_board[item[0]-1][item[1]+1]=='O' and connect_4_board[item[0]-2][item[1]+2]=='O'):
            no_of_o_3_connected+=1
        elif (connect_4_board[item[0]][item[1]]=='O' and ((connect_4_board[item[0]-1][item[1]+1]=='O' and connect_4_board[item[0]-2][item[1]+2]=='.') or (connect_4_board[item[0]-1][item[1]+1]=='.' and connect_4_board[item[0]-2][item[1]+2]=='O')) and connect_4_board[item[0]-3][item[1]+3]=='O'):
            no_of_o_3_connected+=0.75
    return no_of_x_3_connected,no_of_o_3_connected