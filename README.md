# pepper-narrator
HRI Project - Sapienza (AIRO) 2023/2024

---
## Table of content
- [Introduction](#introduction)
- [Resources](#resources)
---


# Introduction

# Resources
To explore some resources used/related to the project look here [resources](resources)

# tmp 
## TODO LIST

- make a series of topics


### How to run a simulation simulation

0. Do once
```
docker network create hri-net --subnet=192.168.1.0/8
```

1. activate docker container
```
systemctl start docker 
docker start pepperhri  --net hri-net --ip 192.168.1.2
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





