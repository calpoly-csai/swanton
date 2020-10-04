#!/bin/sh

if [ ! "$@" ]; then
    echo "USAGE:"
    echo
    echo "./rmdc.sh IMAGE"

    echo
    echo "HERE IS A LIST OF IMAGEs..."
    echo

    sudo docker image list --all

    exit
fi

echo "removing $1 ..."
sudo docker image rm $1 
