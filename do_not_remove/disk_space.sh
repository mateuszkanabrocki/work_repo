#!/bin/bash

disk_used="`df -h | grep /dev/sdb3 | sed "s/ \+/ /g" | cut -d " " -f 5 | cut -b 1-2`"
if [ $disk_used -ge 80 ]; then
    echo "/dev/sdb3 full in $disk_used%"
fi

