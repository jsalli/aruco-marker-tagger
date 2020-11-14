echo === Create Python virtual environment
python -m venv venv
echo === Activate the virtual environment
source venv/bin/activate
echo === Install Python packages
pip install -r requirements.txt
echo =====================
echo INSTALLATION COMPLETE
echo =====================