adduser --gecos "Docker" --home /home/docker --shell /bin/bash --disabled-password docker 
echo -e "docker\ndocker\n" | passwd docker
