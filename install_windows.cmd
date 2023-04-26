@echo off
git pull

set /p PIP_LIBRARIES=<pip.txt
pip install %PIP_LIBRARIES%