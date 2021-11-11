# Kriptografi Tucil 4

## Installing Requirements
### Linux
```bash
virtualenv -p python3 venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows
```bash
python -m virtualenv -p python venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Compiling Extension
```bash
python extension.py
```

then replace line 100 inside `case "EE":` from `JSON.parse(args[0])` to `args[0]`

## Running Extension Debugger
* press F5 to start
* press ctrl + shift + F5 to restart

## Running Command
* press ctrl + p
* type `> Sign` or `> Verify`

