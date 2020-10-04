#!/bin/bash

######################################################################################
#
# installing pip and python and poetry 
#
# if the comments are insufficient, try `explainshell`
# 
# https://explainshell.com/explain?cmd=set+-Eeuo+pipefail
# 
# - source: https://github.com/idank/explainshell 
#
######################################################################################


set -Eeuo pipefail

source /etc/os-release

echo "YOUR SYSTEM INFORMATION..."
cat /etc/os-release
echo "..."
echo "..."

echo "Installing pip & python"

sudo apt-get update -y


sudo apt-get install -y gcc libpq-dev curl 


sudo apt-get install -y python3
sudo apt-get install -y python3-distutils || :  # if the package is not available and the command fails, do nothing,
                                                # the distutils are already installed
sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y
sudo pip3 install --upgrade pip || : #


echo "now get poetry https://python-poetry.org"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3


#
# docker
#

# https://docs.docker.com/engine/install/debian/

echo "setup docker repository"

# remove if already installed, else do nothing
sudo apt-get remove docker docker-engine docker.io containerd runc || : 

sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

echo "install docker engine"

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

echo "now get docker-compose"

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose || :

echo "install docker command-line completion"

sudo curl -L https://raw.githubusercontent.com/docker/compose/1.27.4/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
