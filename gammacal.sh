#!/bin/sh
d=$(dirname $0)
env PYTHONPATH=$d pypenv $0.py $*

