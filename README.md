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

- [X] aggiornare il controllo sulle votazioni
- [X] aggiornare lo stato della pagina web (giorno/notte vivo/morto)
- [ ] fix bug i lupi compaiono nella lista di giocatori da votare nella notte

### How to run a simulation simulation

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





