#!/bin/sh

#lsusb -vv -d 0x0765:0xd094

i=$(lsusb -d 0x0765:0xd094)

if [ "$i" = "" ]; then
  echo "No optix found."
else
  bus=$(echo $i | awk '{print $2}')
  dev=$(echo $i | tr -d : | awk '{print $4}')
  echo "bus=$bus dev=$dev /proc/bus/usb/$bus/$dev"
fi

