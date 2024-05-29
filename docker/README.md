# DOCKER INSTALLATION

## Install [docker](www.docker.com)


Linux version suggested. See also 
[Post-installation steps for Linux](https://docs.docker.com/install/linux/linux-postinstall/),
in particular, add your user to the `docker` group and log out and in again, before proceeding.

* Install docker engine (not docker Desktop!!!)  (tested on v. 19.03, 20.10) 

    Usually, this should work
    
        sudo apt install docker.io

    or install from binaries

        https://docs.docker.com/engine/install/binaries/

    See also 
    [Post-installation steps for Linux](https://docs.docker.com/install/linux/linux-postinstall/).
    In particular, add your user to the `docker` group and log out and in again, before proceeding.

        sudo usermod -aG docker $USER


* Install docker-compose (tested on v. 1.28)

    First remove any other `docker-compose` file, if present (check with `which docker-compose`)

    Download binay file for v. 1.28.5

        cd /usr/local/bin
        sudo wget https://github.com/docker/compose/releases/download/1.28.5/docker-compose-Linux-x86_64
        sudo mv docker-compose-Linux-x86_64 docker-compose
        sudo chmod a+x docker-compose
        docker-compose -v


## Clone this repository

        git clone https://bitbucket.org/iocchi/hri_software.git 


## Configure your system (host OS)

Note: If you want to use different folders, duplicate and modify the `run.bash` script with your own folders. Do not change `run.bash` directly.

1) Download [pepper_tools](https://bitbucket.org/mtlazaro/pepper_tools) in default location `$HOME/src/Pepper/pepper_tools`

    mkdir -p $HOME/src/Pepper
    cd $HOME/src/Pepper
    git clone https://bitbucket.org/mtlazaro/pepper_tools.git 


2) Create a folder `$HOME/playground` that will be shared with the docker container.

    mkdir -p $HOME/playground

This folder will contain permanent files (i.e., files that will survive docker container execution).
Any other file saved in other folders of the docker container will be lost when the container is closed.


3) Update the repository when needed

If needed, update the repositories from your host system

    cd $HOME/src/Pepper/pepper_tools
    git pull

You don't need to make any change in the image, as these folders are mounted from your system and since they contain only Python script code, you do not need to recompile in the container.


## Build an image

Build the latest version

    cd <this_repository>/docker
    ./build.bash 

General command (for special versions)

    cd <this_repository>/docker
    ./build.bash [<version>] [<Dockerfile>] [--no-cache]


Note: `build.bash` script will tag the last built image as `latest`


## Run an image


Run the latest version

    cd <this_repository>/docker
    ./run.bash


General command

    cd <this_repository>/docker
    ./run.bash [<version>]


This docker image uses [tmux](https://github.com/tmux/tmux/wiki) as  terminal multiplexer.


## Access the container

    docker exec -it pepperhri tmux a

You are in the `tmux` environment of the container and you can run tools for connecting to Pepper (robot or emulator).


## Update an image

For permanent changes of your image, when the container is running, you can use

    docker commit <container_name> <image_name>

`<image_name>` can be either a new name or replace the current one


## Delete an image

Images use several GB of disk space. If you want to remove an image you are not using anymore, use the following commands:

    docker image ls
    REPOSITORY                TAG     IMAGE ID         ...
    image-you-want-to-delete  0.0     6b82ade82afd     ...
        
    docker image rm -f <IMAGE ID>


## Cleaning dangling images and containers

    docker image prune
    docker container prune



