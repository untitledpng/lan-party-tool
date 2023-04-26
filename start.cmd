@echo off
for /f "tokens=1* delims==" %%a in ('type .\src\.env ^| findstr /b PYTHON_EXECUTABLE=') do set "python_executable=%%b"

cd ./src
%python_executable% ./main.py
