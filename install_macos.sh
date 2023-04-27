#!/bin/bash

git pull

PIP_LIBRARIES=$(<pip.txt)
pip install $PIP_LIBRARIES

read -n1 -r -p "Press any key to continue..." key