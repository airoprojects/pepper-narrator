#!/bin/bash

SESSION=init

tmux -2 new-session -d -s $SESSION

tmux rename-window -t $SESSION:0 'pepper_tools'
tmux new-window -t $SESSION:1 -n 'naoqi'
tmux new-window -t $SESSION:2 -n 'choregraphe'
tmux new-window -t $SESSION:3 -n 'playground'
tmux new-window -t $SESSION:4 -n 'pepper'

tmux send-keys -t $SESSION:0 "cd src/pepper_tools" C-m
tmux send-keys -t $SESSION:1 "cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64" C-m
tmux send-keys -t $SESSION:1 "./naoqi" C-m
tmux send-keys -t $SESSION:2 "cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64" C-m
tmux send-keys -t $SESSION:2 "./choregraphe --key 654e-4564-153c-6518-2f44-7562-206e-4c60-5f47-5f45" C-m
tmux send-keys -t $SESSION:3 "cd ~/playground/pepper-narrator/utils/ ; python environment.py" C-m

tmux send-keys -t $SESSION:4 "cd ~/playground/pepper-narrator/pepper" C-m
tmux split-window -t $SESSION:4
tmux send-keys -t $SESSION:4 "cd ~/playground/pepper-narrator/pepper" C-m

while [ 1 ]; do
  sleep 60;
done


