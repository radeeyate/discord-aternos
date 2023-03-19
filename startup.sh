#!/bin/bash
CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    echo $token
    echo "TOKEN=$token" > /.env
    echo "USERNAME=$username" >> /.env
    echo "PASSWORD=$password" >> /.env
    echo "DOMAIN=$domain" >> /.env
    echo "ADMIN=$admin" >> /.env
    echo "PREFIX=$prefix" >> /.env
    cat /.env
    pwd
    ls -la
    python3 bot.py
else
    echo "-- Not first container startup --"
    python3 bot.py
fi