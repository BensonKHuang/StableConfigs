#!/bin/bash

# Change these values to fit your machine's absolute path
SRC_DIR="/absolute/path/to/StableConfigs"
VENV_DIR="/absolute/path/to/env"

# Add supervisor directory if doesn't exist 
if [ ! -d /etc/supervisor ]; then
    mkdir /etc/supervisor
fi

# Add supervisor conf.d directory
if [ ! -d /etc/supervisor/conf.d ]; then
    mkdir /etc/supervisor/conf.d
fi

# Add supervisor logging directories 
if [ ! -d /var/log/supervisor ]; then
    mkdir /var/log/supervisor
fi

# Modify the configuration file to use your Path
# Cannot do environment variables in supervisord.conf file 
sed -i.bak 's|SRC_DIR|'$SRC_DIR'|g' supervisord.conf
sed -i.bak 's|VENV_DIR|'$VENV_DIR'|g' supervisord.conf
rm supervisord.conf.bak

# Copy primary supervisor conf file
cp supervisord.conf /etc/supervisor/