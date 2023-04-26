#!/bin/bash

git pull

PIP_LIBRARIES=$(<pip.txt)
pip install $PIP_LIBRARIES