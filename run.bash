eval "$(conda shell.bash hook)"
conda activate simple || echo 'nothing to do!'

### pepper ###
cd ./docker 
gnome-terminal --tab -- ./run.bash 
sleep 5 
gnome-terminal -- ./env.sh
cd ../
echo $(pwd)
##############

### webpage ###
cd ./webserver
python app.py
cd ../
echo $(pwd)
##############


