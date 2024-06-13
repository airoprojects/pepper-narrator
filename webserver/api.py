import json
import time
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
    self.conn, self.addr = None, None
    self.max_votes_allowed = 0
    
  def make_socket(self, host, port):
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_socket.bind((host, port))
      server_socket.listen(1)
      print(f"New socket --> ip: {self.host}, port: {self.port}")
      return server_socket   

  def start_connection(self):
      time.sleep(5)
      print(f"Waiting for a connection... on port {self.port}")
      self.conn, self.addr = self.server_socket.accept() 
    #   return self.server_socket.accept() 

  def listen(self):
    #   conn, addr = self.server_socket.accept()
      while not self.conn:
          pass
      
      print(f"Waiting for docker bridge...")

      with self.conn:
          print('Connected by', self.addr)
          while True:
              data = self.conn.recv(1024)
              if not data:
                  break
              print(f"\nReceived data: {data.decode('utf-8')} \n")
              new_data = json.loads(data.decode('utf-8'))
              self.update_game_info(new_data)
              self.max_votes_allowed = new_data["vote"].count(True)
              self.conn.sendall("New game info received".encode('utf-8'))
      
  def update_game_info(self, new_data):
      self.game_info.clear()
      self.game_info.update(new_data)

  def send_back(self, player_vote):
    #   conn, addr = self.server_socket.accept()
    print(f"Sending data to bridge on port:  {self.port}")
    send_data = json.dumps(player_vote)
    self.conn.sendall(send_data.encode('utf-8'))

    #   return True
  
  def start_listening(self):
        connection_thread = Thread(target=self.start_connection, args=())
        connection_thread.start()
        socket_thread = Thread(target=self.listen, args=())
        socket_thread.start()
        print("all thread running")