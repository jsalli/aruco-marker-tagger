@echo off
ECHO === Create Python virtual environment
call python -m venv venv
ECHO === Activate the virtual environment
call venv\Scripts\activate.bat
ECHO === Install Python packages
call pip install -r requirements.txt
call venv\Scripts\deactivate.bat
ECHO =====================
ECHO INSTALLATION COMPLETE
ECHO =====================
pause
