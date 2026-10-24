#Creates 0-0 scoreboard
def set_score():
  return {'Player X':0,'Player O':0}
def display_score(scoreboard):
  print()
  print(f"Player X has {scoreboard['Player X']} points")
  print(f"Player O has {scoreboard['Player O']} points")
#updates scoreboard
def update_score(player,scoreboard):
  scoreboard[player]+=1
  display_score(scoreboard)