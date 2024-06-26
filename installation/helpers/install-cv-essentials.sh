#!/bin/sh

export DEBIAN_FRONTEND=noninteractive

apt update
apt-get install sudo nano mc ne software-properties-common openssh-server git net-tools -y
apt-get install xauth curl net-tools xvfb x11vnc -y
apt-get install x11-apps glmark2 -y

# # dev tools
apt-get install eog openssh-server git gdb -y
apt-get install cmake cmake-curses-gui pkg-config -y
apt-get install python python3 python3-pip -y

# # tools
apt-get install ffmpeg -y
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev -y
apt-get install libgtk-3-dev libgoogle-glog-dev libgflags-dev -y

# # libs
apt-get install libopencv-dev -y
apt-get install libboost-all-dev -y
