#!/bin/bash

getent passwd docker > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "yes the user exists"
else
   h=/home/docker
   adduser docker --gecos "Docker" --home $h --shell /bin/bash --disabled-password
   echo -e "docker\ndocker\n" | passwd docker
   mkdir -p $h/.ssh 
   chmod 700 $h/.ssh 
   mv /usr/local/bin/id_rsa* $h/.ssh/. 
   cat $h/.ssh/id_rsa.pub > $h/.ssh/authorized_keys
   chmod 600 $h/.ssh/id_rsa && chmod 600 $h/.ssh/id_rsa.pub 
   cp $h/.ssh/id_rsa /export/.dolphinnext/.ssh/1_1_ssh_pri.pky 
   cp $h/.ssh/id_rsa.pub /export/.dolphinnext/.ssh/1_1_ssh_pub.pky
   chown -R docker:docker $h
fi

