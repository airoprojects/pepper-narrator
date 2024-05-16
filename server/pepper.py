import os
import re
import time
import json
# import fcntl
import random
import threading

def check_key(stop_event):
    input("Press Enter to exit the loop.\n")
    stop_event.set()

# stop_event = threading.Event()
# key_thread = threading.Thread(target=check_key, args=(stop_event,))
# key_thread.start()

semaphore_file = 'semaphore.txt'

def set_semaphore(status):
    with open(semaphore_file, 'w') as file:
        # fcntl.flock(file, fcntl.LOCK_EX)  # Acquire exclusive lock
        file.write(status)
        # fcntl.flock(file, fcntl.LOCK_UN)  # Release lock

def get_progressive_id(filename):
  with open(filename, 'r') as file:
    for line in file:
      if '"progressive_id"' in line:
        start = line.find(":") + 1
        end = line.find(",")
        progressive_id = int(line[start:end].strip())
        return progressive_id
  return None

import json

def update_progressive_id(filename, new_id):
  with open(filename, 'r+') as file:
    # Read the first part of the file where "progressive_id" is located
    content = file.read(100)  # Adjust this value if necessary
    
    # Locate the start and end of the "progressive_id" value
    start = content.find('"progressive_id"') + len('"progressive_id": ')
    end = content.find(",", start)
    
    # Build the new content with the updated "progressive_id"
    new_content = content[:start] + str(new_id) + content[end:]
    
    # Move the file pointer to the beginning and write the new content
    file.seek(0)
    file.write(new_content)
    file.flush()


def add_role(current_roles):
  """
  Make a list of roles depending on the number of players
  """
  role = "villager"
  curr_num_players = (len(current_roles) + 1)
  num_of_wolves = current_roles.count("wolf")
  
  # check if there are  enough wolves
  if curr_num_players % 2 == 0:
    wolf_cap = (curr_num_players // 2) - 1  
  else:
    wolf_cap = (curr_num_players // 2)
  if num_of_wolves < wolf_cap:
    role = "wolf"

  # add expansion roles if there are enough players
  if curr_num_players >= 6 and ("seer" not in  current_roles):
    role = "seer"

  if curr_num_players >= 8 and ("medium" not in  current_roles):
    role = "medium"
     
  current_roles.append(role)


def add_players(players, current_roles, max_players, enable_test=False):
   
  # game set-up paramters
  num_players = 0
  min_players = 4
  new_player = False
  pattern = r'[yesi+]+' # input check regex

  while num_players <= max_players:

    playes_info = {}

    if new_player:
      num_players += 1
      qr_code = "player_code " + str(num_players)
      add_role(current_roles)
      playes_info["player_id"] = qr_code
      playes_info["status"] = "alive"
      players.append(playes_info)

    # change this to work with pepper chat
    if num_players < max_players:
      if enable_test: 
        new_player = True
        continue
      new_player = input("Is there another player that want to take part at the game? ").lower()
      new_player = re.fullmatch(pattern, new_player)

    else:
       print("Reached maximum number of players!")
       break

    if num_players < min_players and (not new_player):
       print("Please find some other player. At least 4 people are required to start a game!")
    
    elif num_players >= min_players and (not new_player):
       print("The game is about to start!")
       break

    else:
       pass


def assign_roles(game_dict, players, current_roles):
  random.shuffle(players)
  random.shuffle(current_roles)
  print(players)
  print(current_roles)
  for player, role in zip(players, current_roles):
    player["role"] = role
    game_dict["players"].append(player)


def initialize_game(max_players=8, enable_test=False):

  # parametrs variables
  players = []
  current_roles = []

  # ask the human if start a new game or continue an old one
  new_game = True

  if new_game:
    database_filename = "database.json"

    # set game id
    progressive_id = get_progressive_id(database_filename)
    print(f"Current progressive_id: {progressive_id}")
    new_progressive_id = progressive_id + 1
    print(f"New progressive_id: {new_progressive_id}")

    cache_filename = f"game_{new_progressive_id}_cache.json"

    # initialize cache database for new game
    game_dict = {
        "game_id": new_progressive_id,
        "status": "active",
        "round": 1,
        "night": True,
        "players": []   
    }

  
  add_players(players, current_roles, max_players)
  
  assign_roles(game_dict, players, current_roles)

  # initialize new game file to share info with server 
  with open(cache_filename, "w") as game_file:
    json.dump(game_dict, game_file, indent=4)

  
  ### Here implement the game logic ###

  # update database with final game 
  update_progressive_id(database_filename, new_progressive_id)


if __name__ == "__main__":

  initialize_game()

  # test()

  # # Example: Set the semaphore to green after 10 seconds
  # while not stop_event.is_set():
  #   set_semaphore('green')
  #   print('Semaphore set to green')
  #   time.sleep(10)

  #   set_semaphore('red')
  #   print('Semaphore set to red')
  #   time.sleep(10)


    
  # set_semaphore('red')