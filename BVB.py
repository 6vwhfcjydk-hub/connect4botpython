import Initialisation
import Action
import Outcome
import Display
import AI           # your bot
import claude_bot   # my bot


def your_bot(syb, board, placement):
    return AI.choose_move(syb, board, placement)


def my_bot(syb, board, placement):
    return claude_bot.choose_move(board, syb)


def play(first, second, names):
    board, placement = Initialisation.initialisation()
    players = [('X', first, names[0]), ('O', second, names[1])]
    turn = 0
    while True:
        syb, bot, name = players[turn % 2]
        col = bot(syb, board, placement)
        if col is None or not Action.add_piece(syb, col, board, placement):
            print(f"{name} made an illegal move and forfeits")
            return names[(turn + 1) % 2]
        print(f"{name} ({syb}) plays column {col + 1}")
        if Outcome.who_won(board) is not None:
            Display.display_board(board)
            print()
            return name
        if Outcome.board_full(board):
            Display.display_board(board)
            print()
            return 'Draw'
        turn += 1


print("Game 1 winner:", play(your_bot, my_bot, ('Your bot', "Claude's bot")))
print("Game 2 winner:", play(my_bot, your_bot, ("Claude's bot", 'Your bot')))