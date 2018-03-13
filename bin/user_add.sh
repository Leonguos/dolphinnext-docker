#!/bin/bash

getent passwd docker > /dev/null 2&>1

if [ $? -eq 0 ]; then
    echo "yes the user exists"
else
   adduser docker --gecos "Docker" --home /home/docker --shell /bin/bash --disabled-password
   echo -e "docker\ndocker\n" | passwd docker
   su - docker && mkdir ~/.ssh && \ 
   chmod 700 ~/.ssh && \
   mv /usr/local/bin/id_rsa* ~/.ssh/. && \
   cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys && \
   chmod 600 ~/.ssh/id_rsa && chmod 600 ~/.ssh/id_rsa.pub && \
   cp ~/.ssh/id_rsa /export/.dolphinnext/.ssh/1_1_ssh_pri.pky && \
   cp ~/.ssh/id_rsa.pub /export/.dolphinnext/.ssh/1_1_ssh_pub.pky
fi

