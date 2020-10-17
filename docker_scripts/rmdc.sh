#!/bin/sh

if [ ! "$@" ]; then
    echo "USAGE:"
    echo
    echo "./rmdc.sh CONTAINER"

    echo
    echo "HERE IS A LIST OF CONTAINERs..."
    echo

    sudo docker container list --all

    exit
fi

echo "removing $1 ..."
sudo docker container rm $1 
