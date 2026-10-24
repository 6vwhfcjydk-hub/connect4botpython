#Interface
import Score
import Gameloop
import replay
#Endscreen
def endscreen(movedict):
    while True:
        try:
            x=input('Wish to revisit any one of your games in this matchup? ' \
                    'Type in the game number to see the list of moves played by you and your opponent.' \
                        ' Type exit to exit this screen ')
            x=int(x)
            replay.replay_game(movedict[x])
            print('Notation for game')
            print(movedict[x])
        except ValueError:
            if x.lower().startswith('exit'):
                print('Goodbye!')
                break
            else:
                print('Type in a number or exit the program ')
        except KeyError:
            print('Please enter a valid game number. ')



typ=input('Option 1:Human v Human,Option 2:Human v Robot(1st player), Option 3:Robot v Human(2nd player): Input number 1-3 to select ')
scoreboard = Score.set_score()
print('player X starts first, player O goes second')
print('type "resign" to resign')
movedict=Gameloop.play_game_and_new_game(scoreboard,typ)
endscreen(movedict)