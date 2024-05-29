# Docker file for Human Robot Interaction course
# ROS Melodic, Pepper SDK, Pepper tools, Choregraphe, qibullet
# (https://support.old.unitedrobotics.group/en/support/solutions/articles/80001024221-pepper-2-5-downloads)
# 
# Luca Iocchi, DIAG, Sapienza University of Rome, Italy
# Version 0.8

FROM ros:melodic-ros-base-bionic

ARG DEBIAN_FRONTEND=noninteractive

###### USER root ######

# install libraries and ros packages 

RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tmux less sudo eom wget libwebsockets-dev \
        nano unzip wget iputils-ping net-tools netcat openssh-client \
        bash-completion python-pip \
        ros-melodic-desktop \
        ros-melodic-naoqi-libqi ros-melodic-naoqi-libqicore \
        ros-melodic-naoqi-driver ros-melodic-naoqi-bridge-msgs && \
    rm -rf /var/lib/apt/lists/*



# Pepper

RUN mkdir -p /opt/Aldebaran

# NAOqi SDK

RUN cd /opt/Aldebaran && \
    wget https://community-static.aldebaran.com/resources/2.5.10/NAOqi%20SDK/naoqi-sdk-2.5.7.1-linux64.tar.gz && \
    wget https://community-static.aldebaran.com/resources/2.5.10/Python%20SDK/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz

# Additional packages
#   https://community-static.aldebaran.com/resources/2.5.10/Java%20SDK/java-naoqi-sdk-2.5.6.5-linux64%20%281%29.jar
#   ctc-linux64-atom-2.5.2.74.zip
    

RUN cd /opt/Aldebaran && \
    tar xzvf naoqi-sdk-2.5.7.1-linux64.tar.gz && \
    tar xzvf pynaoqi-python2.7-2.5.7.1-linux64.tar.gz && \
    rm naoqi-sdk-2.5.7.1-linux64.tar.gz && \
    rm pynaoqi-python2.7-2.5.7.1-linux64.tar.gz && \
    cd /opt/Aldebaran/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7 && \
    chmod go+rx site-packages


# Python SDK

ENV PYTHONPATH /opt/Aldebaran/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages

# Choregraphe

RUN cd /opt/Aldebaran && \
    wget https://community-static.aldebaran.com/resources/2.5.10/Choregraphe/choregraphe-suite-2.5.10.7-linux64.tar.gz && \
    tar xzvf choregraphe-suite-2.5.10.7-linux64.tar.gz


###### USER robot ######

# User: robot (password: robot) with sudo power

ARG UID=1000
ARG GID=1000

RUN useradd -ms /bin/bash robot && echo "robot:robot" | chpasswd && adduser robot sudo

RUN usermod -u $UID robot && groupmod -g $GID robot

USER robot

RUN touch ~/.sudo_as_admin_successful
RUN echo "set -g mouse on" > $HOME/.tmux.conf 

RUN mkdir -p $HOME/.config/pulse && \
    cd $HOME/.config/pulse && \
    ln -s /opt/config/pulse/cookie .

RUN pip install --user Pillow tornado==5.1.1 

### Init ROS workspace ###

RUN mkdir -p $HOME/ros/catkin_ws/src

RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; cd $HOME/ros/catkin_ws/src; catkin_init_workspace; cd ..; catkin_make"

RUN echo "source $HOME/ros/catkin_ws/devel/setup.bash\n" >> $HOME/.bashrc

RUN rosdep update


### Additional packages ###

RUN mkdir -p $HOME/src/

# OpenCV
RUN pip install opencv-python==4.2.0.32

# qibullet
RUN pip install --user qibullet==1.2.1

# Pepper tools mounted from local host

VOLUME /home/robot/src/pepper_tools

ENV PEPPER_TOOLS_HOME /home/robot/src/pepper_tools

RUN echo "export PEPPER_IP=127.0.0.1\n" >> $HOME/.bashrc

# Compile ROS packages

RUN /bin/bash -c "source $HOME/ros/catkin_ws/devel/setup.bash; cd $HOME/ros/catkin_ws; catkin_make"



# Patch for Choregraphe

USER root

RUN cd /opt && \
    wget https://github.com/madler/zlib/archive/v1.2.9.tar.gz && \
    tar -zxvf v1.2.9.tar.gz && \
    cd zlib-1.2.9 && \
    ./configure && \
    make && \
    cp /opt/zlib-1.2.9/libz.so.1.2.9  /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64/lib/ && \
    cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64/lib/ && \
    rm libz.so.1.2.8 libz.so.1 libz.so && \
    ln -s libz.so.1.2.9 libz.so.1 && \
    ln -s libz.so.1.2.9 libz.so


USER robot

ADD init.bash /home/robot/init.bash

# Set working dir and container command

WORKDIR /home/robot

CMD [ "bash", "-ci", "/home/robot/init.bash" ]


