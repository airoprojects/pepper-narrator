import os
import re
import time
import json
import random
import threading

from utils import save_data_to_json

def recovery_game_handler(game_id, tts, memory, dialog, database, game_info):
    tts.say("Let me check if game #" + str(game_id) + " can be restored...")
    
    if str(game_id) in database['games']:
        game = database['games'][str(game_id)]
        if game['status'] == 'active':
            for key, value in game.items():
                game_info[key] = value
            dialog.gotoTag("end_init_old", "game_initialization")
        else:
            tts.say("Recovery is not always possible, everything has an end.")
            dialog.gotoTag("endedGameId", "game_initialization")
    else:
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
        "round": 0,
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


def get_votation(memory):
    while memory.getData('votes') == None: time.sleep(0.5)
    return memory.getData('votes')


def game(game_info, tts, memory, dialog, database, logger):
    game_initialization_topic =  '/home/robot/playground/pepper-narrator/pepper/topics/game_loop.top'
    topic_name = dialog.loadTopic(game_initialization_topic)
    dialog.activateTopic(topic_name)
    dialog.subscribe('game_loop')
    winning_team = None
    
    print(game_info['players'])
    print(game_info['roles'])
    
    while memory.getData("state") == "game_loop":
        game_info['round'] += 1
        memory.insertData('game_info', game_info)
        print("Round {}, {}".format(game_info['round'], "night" if game_info['night'] else "day"))
        
        if game_info['night']:
            tts.say("It is night, close your eyes.")
            memory.insertData('votes', None) 
            memory.insertData("game_state", "voting_night") # for server callback
            tts.say("Wolves, you have to choose your victim.")
            print("changed game state")
            
            player_to_kill = get_votation(memory)
            
            game_info['alive'][player_to_kill] = False
            player_to_kill_name =  game_info['players'][player_to_kill]
            tts.say("The sun is rising. You can open your eyes again.")
            tts.say("I\'m so sorry to tell you that {} is dead, what a tragedy.".format(player_to_kill_name.upper()))
            game_info['night'] = False
            print(player_to_kill, player_to_kill_name)
            print(game_info['alive'])
            
        else:
            tts.say("Now you must decide who is responsible for this!")
      
            majority = False
            while not majority:
                memory.insertData('votes', None) 
                memory.insertData("game_state", "voting_day") # for server callback
                
                players_votes = get_votation(memory)                

                max_votes = max(players_votes)
                print(max_votes, players_votes)
                if players_votes.count( max_votes ) > 1:
                    print("again")
                    tts.say("Please vote again. You must be more united in your choice.")
                    tts.say("X and Y, what do you have to say about your innocence?") # TODO improve using names of most voted players
                else:
                    majority = True
                    player_to_kill = players_votes.index(max_votes) 
                    player_to_kill_name =  game_info['players'][player_to_kill]
                    tts.say("So you all agree that {} is responsible, interesting...".format(player_to_kill_name.upper()))
                    game_info['alive'][player_to_kill] = False
                    game_info['night'] = True
                    print(player_to_kill, player_to_kill_name)
                    print(game_info['alive'])
        
        alive_wolves = [ game_info["roles"][i] == "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
        alive_no_wolves = [ game_info["roles"][i] != "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
        print("alive villagers: {}".format(alive_no_wolves))
        print("alive wolves: {}".format(alive_wolves))  
        # stop conditions
        if alive_wolves == 0 :
            winning_team = "villagers"
            dialog.gotoTag("end", "game_loop")
            tts.say("Villagers win")
            memory.insertData("game_state", "end")
            memory.insertData("winning_team", winning_team)
        elif alive_wolves >= alive_no_wolves:
            winning_team = "wolves"
            dialog.gotoTag("end", "game_loop")
            tts.say("Wolves win")
            memory.insertData("game_state", "end")
            memory.insertData("winning_team", winning_team)
    
    if memory.getData("state") == "end":
        # termination
        game_info['status'] = "inactive"
        game_info['winning_team'] = winning_team
        database['games'][ str(game_info['game_id']) ] = game_info
        for i in range(len(game_info['players'])):
            player_name = game_info['players'][i]
            if winning_team == 'wolves' and game_info['roles'][i] == 'wolf':
                database['players'][player_name]['victories'] += 1
            elif winning_team == 'villagers' and game_info['roles'][i] != 'wolf':
                database['players'][player_name]['victories'] += 1
        print("saved stats for game #{}".format(game_info['game_id']))
    else:
        while memory.getData("state") == "paused": time.sleep(0.1)
        if memory.getData("state") == "save": 
            database['games'][ str(game_info['game_id']) ] = game_info
            
    dialog.unsubscribe('game_loop')
    dialog.deactivateTopic(topic_name)
    dialog.unloadTopic(topic_name)
    
