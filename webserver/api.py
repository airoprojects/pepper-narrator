import json
import socket
from copy import deepcopy
from threading import Thread

#api between server(flask)-bridge
class API():

  def __init__(self, host = '192.168.60.17', port = 65432, game_info = {}):
    # Socket configuration
    self.host = host
    self.port = port
    self.game_info = game_info
    self.server_socket = self.make_socket(host, port)
    
        
    
  def make_socket(self, host, port):
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_socket.bind((host, port))
      server_socket.listen(1)
      print(f"New socket --> ip: {self.host}, port: {self.port}")
      return server_socket      

  def listen(self):
      print(f"Waiting for a connection... on port {self.port}")
      conn, addr = self.server_socket.accept()

      with conn:
          print('Connected by', addr)
          while True:
              data = conn.recv(1024)
              if not data:
                  break
              print(f"\nReceived data: {data.decode('utf-8')} \n")
              new_data = json.loads(data.decode('utf-8'))
              self.update_game_info(new_data)
              conn.sendall("Data received".encode('utf-8'))
              # self.game_info = deepcopy(data.decode('utf-8'))
              # conn.sendall("Data received".encode('utf-8'))
              # self.game_info = json.loads(self.game_info)
      
  def update_game_info(self, new_data):
      self.game_info.clear()
      self.game_info.update(new_data)

  def send_back(self, player_vote):
      conn, addr = self.server_socket.accept()
      print(f"Sending data to bridge {self.port}")

      with conn:
        # print("Sending data to bridge")
        send_data = json.dumps(player_vote)
        conn.sendall(send_data.encode('utf-8'))
        # reset player vote dictionary
        # num_votes = 0 
        # player_vote = {}
      return True
  
  def start_linking(self):
     socket_thread = Thread(target=self.listen, args=())
     socket_thread.start()
     print("end linking")