import os
import re
import time
import json
import random
import threading

def update_state_night(
    game_info, 
    player_to_kill, 
    cache_filename, 
    alive_no_wolves
):
  
  for player in game_info['players']:
    is_alive = (player['status'] == "alive")

    if is_alive and player['player_id'] == player_to_kill:
      if player['role'] == "wolf":
        # TODO: send this message to the client 
        raise  Exception("Error: wolves cannot kill each others")
      
      print("killing: {}".format(player['player_id']))
      player['status'] = "dead"
      alive_no_wolves -= 1
      break

  # update the state of the game
  game_info['night'] = False
  # save_data_to_json(cache_filename, game_info)


def update_state_day(game_info, players_votes, cache_filename):
  candidates = []
  max_votes = max(players_votes.values())

  # check for the players with the maximum nuber of votes
  for player, votes in players_votes.items():
    if votes == max_votes:
      candidates.append(player)
  
  # 
  for player in game_info['players']:
    if player['player_id'] in players_votes.keys():
      votes = players_votes[player['player_id']]
      player['votes'] = votes
      if votes == max_votes :
        candidates.append(player['player_id'])

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
  # save_data_to_json(cache_filename, game_info)


def game(game_info, alive_wolves, alive_no_wolves, cache_filename):
  
  while True:

    # just for debug
    print("alive villagers: {}".format(alive_no_wolves))
    print("alive wolves: {}".format(alive_wolves))
  
    # TODO: implement here the game logic 
    # TODO: wait for the response from the web
    # TODO: get id of player_to kill

    # with open(cache_filename, "r") as game_file:
    #   game_info = json.load(game_file)

    # game_info = load_data_from_json(cache_filename)

    if game_info['night']:
      player_to_kill = "player_code_2" # to get from the web
      update_state_night(
        game_info, 
        player_to_kill, 
        cache_filename,
        alive_no_wolves,
      )

    # update the state of all the players during night
    # if game_info['night']:
    #   for player in game_info['players']:
    #     is_alive = (player['status'] == "alive")
    #     if is_alive and player['player_id'] == player_to_kill:
    #       # if player['role'] == "wolf":
    #       #   # TODO: send this message to the client 
    #       #   raise  Exception("Error: wolves cannot kill each others")
    #       print("killing: {}".format(player['player_id']))
    #       player['status'] = "dead"
    #       alive_no_wolves -= 1
    #       break

    # # update the state of the game
    # game_info['night'] = False
    # save_data_to_json(cache_filename, game_info)
    
    else:
      # TODO: get a list of votes for each charater form the web page
      players_votes = {"player_code_1": 5}
      update_state_day(
        game_info, 
        players_votes, 
        cache_filename,
        alive_wolves, 
        alive_no_wolves
      )

    # for player in game_info['players']:
    #   if player['player_id'] in foo.keys():
    #     player['votes'] = foo[player['player_id']]

    # # update the state of all the players during day
    # if not game_info['night']:
    #   # TODO: filter the players that are alive with the majority of votes
    #   candidates = filter(
    #     lambda x: (
    #       x['votes'] == max(
    #         game_info['players'], key=lambda y: y['votes']
    #       )['votes']
    #       and 
    #       x['status'] == "alive"
    #     ),
    #     game_info['players']
    #   )

    #   candidates = list(candidates)
    #   if len(candidates) == 1:
    #     candidate_id = game_info['players'].index(candidates[0])
      
    #   else:
    #     # TODO: here notify the client to do anoter voting
    #     pass

    #   game_info['players'][candidate_id]['status'] = "dead"
    #   if game_info['players'][candidate_id]['role'] == "wolf":
    #     alive_wolves -= 1
    #   else:
    #     alive_no_wolves -= 1
    
    # # update the state of the game
    # save_data_to_json(cache_filename, game_info)

    # stop condiction
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
  # save_data_to_json(cache_filename, game_info)


if __name__ == "__main__":

  game()
