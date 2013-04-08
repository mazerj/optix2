#!/bin/sh
P=$(dirname $(dirname $(which pype)))
sudo $P/bin/pypenv `which gammacal`.py $*

