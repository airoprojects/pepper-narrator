import os
import sys
import json

def load_data_from_json(filename):
  data = None
  with open(filename, 'r') as f:
    data = json.load(f)
  return data

def save_data_to_json(filename, data):
  with open(filename, "w") as f:
    json.dump(data, f, indent=4)

def reset_memory(memory):
    keys_to_remove = ["database_filename", "state", "violence","game_state"]  # Aggiungi tutte le chiavi che vuoi resettare qui
    for key in keys_to_remove:
        try:
            memory.removeData(key)
            print("Removed key:")
            print(key)
        except Exception as e:
            print("coult not remove key:")
            print(key)
            print("error:")
            print(e)
    print("Memory reset completed.")