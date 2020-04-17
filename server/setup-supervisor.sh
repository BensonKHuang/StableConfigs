#!/bin/bash
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

# Copy primary supervisor conf file
cp configs/supervisord.conf /etc/supervisor/

# Copy program supervisor conf files
cp configs/conf.d/*.conf /etc/supervisor/conf.d/