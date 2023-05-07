@ECHO OFF
pip install --user -r requirements.txt
CLS
CD %~dp0
IF NOT EXIST logs (
	MKDIR logs
)
python app.py
PAUSE