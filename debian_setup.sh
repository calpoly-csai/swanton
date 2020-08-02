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
