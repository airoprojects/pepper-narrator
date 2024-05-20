import os
import re
import time
import json
import random
import threading

from utils import load_data_from_json, save_data_to_json

def get_progressive_id(filename):
  with open(filename, 'r') as file:
    for line in file:
      if '"progressive_id"' in line:
        start = line.find(":") + 1
        end = line.find(",")
        progressive_id = int(line[start:end].strip())
        return progressive_id
  return None

def update_progressive_id(filename, new_id):
  with open(filename, 'r+') as file:
    # Read the first part of the file where "progressive_id" is located
    content = file.read(100) 
    
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


def add_players(players, current_roles, max_players, tts, memory, dialog, logger, enable_test=False):
   
  # game set-up paramters
  num_players = 0
  min_players = 4
  new_player = False
  pattern = r'[yesi+]+' # input check regex

  while num_players <= max_players:

    player_info = {}

    if new_player:
      num_players += 1
      qr_code = "player_code_" + str(num_players)
      add_role(current_roles)
      player_info['player_id'] = qr_code
      player_info['status'] = "alive"
      player_info['votes'] = 0
      
      players.append(player_info)

    # TODO: change this to work with pepper chat -> dialog in Choregraphe
    if num_players < max_players:
      if enable_test: 
        new_player = True
        continue
      new_player = raw_input("Is there another player that want to take part at the game? ").lower()
      new_player = re.match(pattern, new_player)

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


def assign_roles(
    game_info, 
    players, 
    current_roles, 
    alive_wolves, 
    alive_no_wolves
):
  random.shuffle(players)
  random.shuffle(current_roles)

  for player, role in zip(players, current_roles):
    player['role'] = role
    game_info['players'].append(player)

    if role == "wolf": alive_wolves += 1
    else: alive_no_wolves += 1


def initialize_game(tts, memory, dialog, database, logger, max_players=8, enable_test=False):

  # game parametrs
  players = []
  current_roles = []
  alive_wolves = 0
  alive_no_wolves = 0
  
  # TODO: ask the human if start a new game or continue an old one
  new_game = True

  if new_game:

    # set game id
    progressive_id = database['progressive_id']
    logger.info("Current progressive_id: {}".format(progressive_id))
    new_progressive_id = progressive_id + 1
    database['progressive_id'] += 1
    logger.info("New progressive_id: {}".format(new_progressive_id))

    cache_filename = "game_{}_cache.json".format(new_progressive_id)

    # initialize cache database for new game
    game_info = {
        "game_id": new_progressive_id,
        "status": "active",
        "round": 1,
        "night": True,
        "players": []   
    }
  
  else:
    # TODO: load old game
    pass

  add_players(players, current_roles, max_players, tts, memory, dialog, logger)
  
  assign_roles(
    game_info, 
    players, 
    current_roles, 
    alive_wolves, 
    alive_no_wolves
  ) 
  save_data_to_json(cache_filename, game_info) # initialize new game
  
  return (game_info, alive_wolves, alive_no_wolves)
  

def game(game_info, alive_wolves, alive_no_wolves, cache_filename):
  
  while True:

    print("alive villagers: {}".format(alive_no_wolves))
    print("alive wolves: {}".format(alive_wolves))
  
    # TODO: implement here the game logic 
    # TODO: wait for the response from the web
    # TODO: get id of player_to kill

    player_to_kill = "player_code_2" # to get from the web

    with open(cache_filename, "r") as game_file:
      game_info = json.load(game_file)

    # update the state of all the players during night
    if game_info['night']:
      for player in game_info['players']:
        is_alive = (player['status'] == "alive")
        if is_alive and player['player_id'] == player_to_kill:
          # if player['role'] == "wolf":
          #   # TODO: send this message to the client 
          #   raise  Exception("Error: wolves cannot kill each others")
          print("killing: {}".format(player['player_id']))
          player['status'] = "dead"
          alive_no_wolves -= 1
          break

    # update the state of the game
    game_info['night'] = False
    save_data_to_json(cache_filename, game_info)
    
    # TODO: get a list of votes for each charater form the web page
    foo = {"player_code_1": 5}

    for player in game_info['players']:
      if player['player_id'] in foo.keys():
        player['votes'] = foo[player['player_id']]

    # update the state of all the players during day
    if not game_info['night']:
      # TODO: filter the players that are alive with the majority of votes
      candidates = filter(
        lambda x: (
          x['votes'] == max(
            game_info['players'], key=lambda y: y['votes']
          )['votes']
          and 
          x['status'] == "alive"
        ),
        game_info['players']
      )

      candidates = list(candidates)
      if len(candidates) == 1:
        candidate_id = game_info['players'].index(candidates[0])
      
      else:
        # TODO: here notify the client to do anoter voting
        pass

      game_info['players'][candidate_id]['status'] = "dead"
      if game_info['players'][candidate_id]['role'] == "wolf":
        alive_wolves -= 1
      else:
        alive_no_wolves -= 1
    
    # update the state of the game
    save_data_to_json(cache_filename, game_info)

    # TODO: check for stop condictions
    if alive_wolves <= 0 :
      # TODO: make pepper say this
      print("villagers win")
      break
    elif alive_wolves > alive_no_wolves:
      # TODO: make pepper say this
      print("wolves win")
      break

    game_info['round'] += 1
    break


    # end of loop

  # termination
  game_info['status'] = "inactive"
  save_data_to_json(cache_filename, game_info)



if __name__ == "__main__":

  initialize_game()
