## Prerequisities

- Python 3.6 or newer
- Pip https://pip.pypa.io/en/stable/installing/

## First Run

In the project folder:

1. `python3 -m venv venv` - Creating a virtual environment for installing dependencies locally.
2. `source venv/bin/activate` (Linux, MacOS), or `activate.bat` in `venv/Scripts` (Windows) - Switching to the virtual environment.
3. `pip install -r requirements.txt` - Installing all necessary dependencies defined in txt file.
4. `rasa run actions` - Running a custom action connecting to geo data. Keep this server running.
5. `rasa train` - Training intents and dialogues.
6. `rasa x` - Testing and improving the bot via web GUI.

## Testing

The chatbot can react to `hi` or `hello`.

The chatbot can find the most populous city of a country by typing e.g.:
`What is the most populous city of Zimbabwe?` It uses SPARQL API to find the answer in the Wikidata Knowledge Base (https://query.wikidata.org/), see `actions.py`. It may take up to 15 secs to find the answer.
