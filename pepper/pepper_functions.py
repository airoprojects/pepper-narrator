import os
import re
import sys
import time
import json
import random
import threading
from functools import partial
import animations


# add project root to sys path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from utils.utils import save_data_to_json


def recovery_game_handler(game_id, tts, motion, memory, dialog, database, game_info):
    animations.general_talking(tts, motion, "Let me check if game #" + str(game_id) + " can be restored...")
    
    if str(game_id) in database['games']:
        game = database['games'][str(game_id)]
        if game['status'] == 'active':
            for key, value in game.items():
                game_info[key] = value
            dialog.gotoTag("end_init_old", "game_initialization")
        else:
            animations.general_talking(tts, motion, "Recovery is not always possible, everything has an end.")
            dialog.gotoTag("endedGameId", "game_initialization")
    else:
        animations.general_talking(tts, motion, "Do not lie to me, this game never existed.")
        dialog.gotoTag("wrongGameId", "game_initialization")
    

def new_player_handler(last_player_name, tts, motion, memory, dialog, database, max_players, game_info):

    if(last_player_name in game_info['players']):
        animations.general_talking(tts, motion, last_player_name + ", you are already registered.")
        dialog.gotoTag("name", "game_initialization")
        return None
    elif(last_player_name in database['players']):
        # TODO check if is the same player or a new one with the same name -> ask to insert a new username
        animations.general_talking(tts, motion, last_player_name + ", Nice to see you again...")
        database['players'][last_player_name]['games'] += 1
    else:
        animations.general_talking(tts, motion, last_player_name + ", nice to meet you...")
        database['players'][last_player_name] = {}
        database['players'][last_player_name]['games'] = 1
        database['players'][last_player_name]['victories'] = 0
        database['players'][last_player_name]['genre'] = random.choice(['Male','Female'])
    
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


def explain_game(tts, motion, dialog, memory):
    print('chatgpt help us')
    tts.say("test spiegazione")
    animations.general_talking(tts, motion, 
        """
            In Lupus in Tabula, each player is secretly assigned a role, such as a Werewolf, Villager, or a special character like the Seer or Witch. I will be the non-playing moderator, overseeing the game to ensure the rules are followed and guiding the narrative. \\

            The game is divided into two phases: night and day. During the night phase, the Werewolves secretly choose a victim to eliminate, while special characters, like the Seer who can identify a player's role, may use their unique abilities.

            When the day phase begins, everyone discusses who they think the werewolves are. You all will vote, and the player with the most votes will be lynched, revealing their role. This cycle continues, with players being eliminated and revealing their roles, until one side wins. The Werewolves win by reducing the number of villagers to equal their own, while the villagers win by identifying and eliminating all the werewolves.

            As the narrator, I'll oversee the game, making sure everything runs smoothly and providing the necessary prompts and narrative to keep the game engaging. The game is heavily based on discussion, bluffing, and deduction, so be ready for a mix of strategy and social interaction. Special roles like the Seer and Witch will add unique twists that can influence the game's outcome. We'll continue alternating between night and day phases until either the werewolves or villagers achieve their win condition.
        """
    )
    memory.insertData("state", "initialization")
    dialog.gotoTag("selection", "game_initialization")


def initialize_game(tts, memory, dialog, database, logger, motion, max_players=8):
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
        "alive": [],
        "vote": [],
        "hist": [],
    }
    
    subscriber_name = memory.subscriber("last_player_name") 
    connection_name = subscriber_name.signal.connect(lambda name: new_player_handler(name, tts, motion, memory, dialog, database, max_players, game_info))
    subscriber_recovery = memory.subscriber("recovered_game_id")
    connection_recovery = subscriber_recovery.signal.connect(lambda name: recovery_game_handler(name, tts, motion, memory, dialog, database, game_info))
    while memory.getData("state") not in ["ready_new", "ready_old", "end"]:
        if memory.getData("state") == 'explain': explain_game(tts, motion, dialog, memory)
        time.sleep(0.5)
    
    # cleaning ALDialog connection and deactivating initialization topic        
    subscriber_name.signal.disconnect(connection_name)
    subscriber_recovery.signal.disconnect(connection_recovery)
    dialog.unsubscribe('game_initialization')
    dialog.deactivateTopic(topic_name)
    dialog.unloadTopic(topic_name)
    
    if memory.getData("state") == "ready_new":
        game_info["alive"] = [True for players in game_info["players"]]
        game_info["vote"] = [False for players in game_info["players"]]
        game_info["roles"] = assign_roles(game_info["players"])
        database['progressive_id'] += 1
    
    return game_info


def get_votation(memory, tts, warnings, motion, game_info, license):
    while memory.getData('votes') == None: 
        if (memory.getData('violence') == 'true' and warnings <= 3 ):
            tts.say("Please please lets keep the game enjoiable for everyone!")   
            memory.insertData('violence', 'false')
            animations.calm_down(motion) 
            animations.start_pose(motion)
            warnings += 1

            if warnings >= 3 : 
                tts.say("Hey! You are losing track of the goal, we are here to have fun not to insult and discuss \nI fell that is better to pause the game for the moment and start back after everyone has calmed down. Fell free to talk to me ") 
                memory.insertData("game_state", "save")
                animations.head_no(motion)
                animations.start_pose(motion)
                animations.hello(motion)
                animations.start_pose(motion)
                break

        if (memory.getData('time') == 'true'):
            late_players = memory.getData('late_players')
            animations.general_talking(tts, motion, late_players + " please hurry up, the others are wating for you!!!")  
            memory.insertData('time', 'false')
            memory.insertData('late_players', '')

        # if (memory.getData('joke') == 'true' and game_info['hist'] != []):
        if (memory.getData('joke') == 'true' ):
            # max_index = game_info['hist'].index(max(game_info['hist']))
            player_name = "leo" #game_info['players'][max_index]
            tts.say("Hey "+ player_name + " it seems the other are very suspicious about you, may I ask why, what did you do to them? :) ")

            animations.joke_around(motion)
            time.sleep(3)
            animations.start_pose(motion)
            memory.insertData('joke', 'false')
            
        time.sleep(0.5)
    return memory.getData('votes')


def violence_handler(a, tts, motion, memory, dialog, database, game_info):
    if(a == 'ciao'): 
        tts.say("ve ne passate sempre. Bastardi figli di puttana")   
        animations.calm_down(motion) 
        animations.start_pose(motion)
         


def game(game_info, tts, motion, memory, dialog, database, logger):
    game_initialization_topic =  '/home/robot/playground/pepper-narrator/pepper/topics/game_loop.top'
    topic_name = dialog.loadTopic(game_initialization_topic)
    dialog.activateTopic(topic_name)
    dialog.subscribe('game_loop')
    winning_team = None
    warnings = 0
    
    # env initializations
    memory.insertData('violence', 'false')
    memory.insertData('time', 'false')
    memory.insertData('joke', 'false')
    memory.insertData('opened_eyes', 'false')

    print(game_info['players'])
    print(game_info['roles'])

    # subscriber_violence = memory.subscriber('violence')
    # connection_violence = subscriber_violence.signal.connect(lambda a: violence_handler(a, tts, motion, memory, dialog, database, game_info))

    # setup license
    license = dict()
    for player in game_info['players']: license[player] = 100
    
    while memory.getData("state") == "game_loop":
        time.sleep(0.5)
        # print('v:',  memory.getData('violence'))
        game_info['round'] += 1
        # TODO: send to socket
        memory.insertData('game_info', game_info)
        print("Round {}, {}".format(game_info['round'], "night" if game_info['night'] else "day"))
        
        if game_info['night']:
            animations.general_talking(tts, motion, "It is night, close your eyes.")
            memory.insertData('votes', None) 

            # wolves can now vote
            for idx, value in enumerate(zip(game_info["roles"], game_info["alive"])):
                role, alive = value
                if role == "wolf" and alive: game_info["vote"][idx] = True
            animations.general_talking(tts, motion, "Wolves, you have to choose your victim.")

            # uptate game info to tell web page who can vote
            memory.insertData('game_info', game_info)
            print("changed game state")
            print("who can vote: ", game_info["vote"])
            memory.insertData("game_state", "voting_night") # for server callback
            
            player_to_kill = get_votation(tts, motion, warnings, motion, game_info, license)
            if player_to_kill == None: break
            
            game_info['alive'][player_to_kill] = False
            player_to_kill_name =  game_info['players'][player_to_kill]
            animations.general_talking(tts, motion, "The sun is rising. You can open your eyes again.")
            animations.general_talking(tts, motion, "I\'m so sorry to tell you that {} is dead, what a tragedy.".format(player_to_kill_name.upper()))
            game_info['night'] = False
            
            # disable vote
            game_info["vote"] = [False for players in game_info["players"]]
            
            print(player_to_kill, player_to_kill_name)
            print(game_info['alive'])
            
        else: # day

            # everyone can now vote
            for idx, alive in enumerate(game_info["alive"]):
                if alive: game_info["vote"][idx] = True
            animations.general_talking(tts, motion, "Now you must decide who is responsible for this!")

            memory.insertData('game_info', game_info)
            majority = False
            round = 0
            while not majority:
                round += 1
                memory.insertData('votes', None) 
                memory.insertData("game_state", "voting_day") # for server callback

                players_votes = get_votation(memory, tts, warnings, motion, game_info, license) # suppose that this list is complete !!!  
                print("INFO players votes: ", players_votes) 

                # make a function for this
                if game_info['hist'] == [] : game_info['hist'] = players_votes
                else: game_info['hist'] = [x + y for x, y in zip(game_info['hist'], players_votes)]

                print("INFO: ", game_info['hist'])
                if players_votes == None: break    
                max_votes = max(players_votes)
                print(max_votes, players_votes)

                if players_votes.count( max_votes ) > 1:
                    print("again")
                    animations.general_talking(tts, motion, "Please vote again. You must be more united in your choice.")
                    tie_players = [id for id in range(len(players_votes)) if players_votes[id] == max_votes]
                    msg = " ".join(game_info['player'][id] for id in tie_players) + "what do you have to say about your innocence?"
                    animations.general_talking(tts, motion, msg) # TODO improve using names of most voted players
                    # animations.general_talking(motion, tts, "X and Y, what do you have to say about your innocence?") # TODO improve using names of most voted players
                    # disable voting for tie players
                    for id in tie_players:
                        game_info['vote'][id] = False
                    memory.insertData("game_state", "voting_day_"+str(round))
                else:
                    majority = True
                    player_to_kill = players_votes.index(max_votes) 
                    player_to_kill_name =  game_info['players'][player_to_kill]
                    animations.general_talking(tts, motion, "So you all agree that {} is responsible, interesting...".format(player_to_kill_name.upper()))
                    game_info['alive'][player_to_kill] = False
                    game_info['night'] = True
                    print(player_to_kill, player_to_kill_name)
                    print(game_info['alive'])

            # disable vote
            game_info["vote"] = [False for players in game_info["players"]]
        
        alive_wolves = [ game_info["roles"][i] == "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
        alive_no_wolves = [ game_info["roles"][i] != "wolf" and game_info["alive"][i] for i in range(len(game_info["players"])) ].count(True)
        print("alive villagers: {}".format(alive_no_wolves))
        print("alive wolves: {}".format(alive_wolves))  

        # stop conditions
        if alive_wolves == 0 :
            winning_team = "villagers"
            dialog.gotoTag("end", "game_loop")
            animations.general_talking(motion, tts, "Villagers win")
            memory.insertData("game_state", "end")
            memory.insertData("winning_team", winning_team)

        elif alive_wolves >= alive_no_wolves:
            winning_team = "wolves"
            dialog.gotoTag("end", "game_loop")
            animations.general_talking(motion, tts, "Wolves win")
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






