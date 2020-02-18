## First Run

1. `python3 -m venv venv` - Creates a virtual environment for installing dependencies locally.
2. `source venv/bin/activate` or `activate.bat` in `venv/Scripts` - Switching to the virtual environment.
3. `pip install -r requirements.txt` - Installing all necessary dependencies defined in txt file.
4. `rasa run actions` - Running a custom action connecting to geo data. Keep this server running.
5. `rasa train` - Training intents and dialogues.
6. `rasa x` - Test and improve bot via web GUI.
