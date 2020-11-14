@echo off
ECHO === Activate the virtual environment
call venv\Scripts\activate.bat
ECHO === Start Aruco tagger
start cmd /k python aruco_tagger.py
exit