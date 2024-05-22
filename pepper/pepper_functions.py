import os
import re
import time
import json
import random
import threading

from utils import load_data_from_json, save_data_to_json

def recovery_game_handler(game_id, tts, memory, dialog, database, game_info):
    tts.say("Let me check if game #" + str(game_id) + " can be restored...")
    
    for game in database['games']:
        if str(game['game_id']) == game_id:
            if game['status'] == 'active':
                for key, value in game.items():
                    game_info[key] = value
                dialog.gotoTag("end_init_old", "game_initialization")
            else:
                tts.say("Recovery is not always possible, everything has an end.")
                dialog.gotoTag("endedGameId", "game_initialization")
            return None
            
    tts.say("Do not lie to me, this game never existed.")
    dialog.gotoTag("wrongGameId", "game_initialization")
    

def new_player_handler(last_player_name, tts, memory, dialog, database, max_players, game_info):
    if(last_player_name in game_info['players']):
        tts.say(last_player_name + ", you are already registered.")
        dialog.gotoTag("name", "game_initialization")
        return None
    elif(last_player_name in database['players']):
        # TODO check if is the same player or a new one with the same name -> ask to insert a new username
        tts.say(last_player_name + ", Nice to see you again...")
        database['players'][last_player_name]['games'] += 1
    else:
        tts.say(last_player_name + ", nice to meet you...")
        database['players'][last_player_name] = {}
        database['players'][last_player_name]['games'] = 1
        database['players'][last_player_name]['victories'] = 0
    
    game_info['players'].append(last_player_name)
    
    registered_players = memory.getData("registered_players") + 1
    memory.insertData("registered_players", registered_players)
    next_player_id = int(memory.getData("next_player_id")) + 1
    memory.insertData("next_player_id", next_player_id)
    
    if registered_players < 4: dialog.gotoTag("name", "game_initialization")
    elif registered_players < max_players: dialog.gotoTag("ask_more_players", "game_initialization")
    else: dialog.gotoTag("full", "game_initialization")


def assign_roles(players):
    num_players = len(players)
    num_wolves = num_players // 2 if (num_players % 2 != 0) else num_players // 2 - 1
    roles = ['wolf'] * num_wolves
    if(num_players >= 6): roles.append('seer')
    if(num_players >= 8): roles.append('medium')
    roles += ['villager'] * (num_players - len(roles))
    random.shuffle(roles)
    return roles


def initialize_game(tts, memory, dialog, database, logger, max_players=8):
    game_initialization_topic =  '/home/robot/playground/pepper-narrator/pepper/topics/game_initialization.top'
    topic_name = dialog.loadTopic(game_initialization_topic)
    dialog.activateTopic(topic_name)
    dialog.subscribe('game_initialization')
    memory.insertData('registered_players', 0)
    
    game_info = {
        "game_id": database['progressive_id'] + 1,
        "status": "active",
        "round": 1,
        "night": True,
        "players": [],
        "roles": [],
        "alive": []
    }
    
    subscriber_name = memory.subscriber("last_player_name")
    connection_name = subscriber_name.signal.connect(lambda name: new_player_handler(name, tts, memory, dialog, database, max_players, game_info))
    subscriber_recovery = memory.subscriber("recovered_game_id")
    connection_recovery = subscriber_recovery.signal.connect(lambda name: recovery_game_handler(name, tts, memory, dialog, database, game_info))
    
    while memory.getData("state") not in ["ready_new", "ready_old", "end"]:
        time.sleep(0.5)
    
    # cleaning ALDialog connection and deactivating initialization topic        
    subscriber_name.signal.disconnect(connection_name)
    subscriber_recovery.signal.disconnect(connection_recovery)
    dialog.unsubscribe('game_initialization')
    dialog.deactivateTopic(topic_name)
    dialog.unloadTopic(topic_name)
    
    if memory.getData("state") == "ready_new":
        game_info["alive"] = [True for players in game_info["players"]]
        game_info["roles"] = assign_roles(game_info["players"])
        database['progressive_id'] += 1
    
    return game_info