#!/bin/sh
P=$(dirname $(dirname $(which pype)))
$P/bin/pypenv `which gammacal`.py $*

