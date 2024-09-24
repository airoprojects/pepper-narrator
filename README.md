# Pepper Narrator
HRI Project - Sapienza (AIRO) 2023/2024

---
## Table of content
- [Introduction](#introduction)
- [How to run](#how-to-run)
- [Resources](#resources)
---


# Introduction
The project involves creating a Human-Robot-Interaction task using Pepper, a semi-humanoid robot, to play the role-playing game "Lupus in fibula" with human participants. The robot interacts with players by using its sensory and communication functions to detect players, monitor emotions, enforce game rules, and maintain an enjoyable atmosphere. It can recognize if players are breaking rules, like keeping their eyes closed when required, and can use dialogue and gestures to engage participants and continue a paused game if needed.

# How to run 
0. Do once
```
docker network create hri-net --subnet=192.168.1.0/8
```

1. activate docker container
```
cd docker 
./run.bash
docker exec -it pepperhri tmux a
```
2. run choreograph in choreograph terminal
```
./choreograph
```
3. run naoqi in naoqi terminal
```
./naoqi
```
4. Connect from choreograph to virtual robot
5. run pepper main in playground terminal
```
cd pepper-narrator/pepper
python main.py
```
6. run the web server
```
cd pepper-narrator/webserver
python app.py
```
7. run the bridge between docker and the host machine
```
cd pepper-narrator/pepper
python bridge.py
```

# Resources
To explore some resources used/related to the project look here [resources](resources)




