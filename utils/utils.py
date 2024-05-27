import os
import sys
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

def load_data_from_json(filename):
  data = None
  with open(filename, 'r') as f:
    data = json.load(f)
  return data

def save_data_to_json(filename, data):
  with open(filename, "w") as f:
    json.dump(data, f, indent=4)