# MealGauge
---
## Running Locally
### Windows (via PowerShell)
```
pip install virtualenv
python3 -m venv env
env/Scripts/activate
pip install -r requirements.txt
cd app
flask run
```

### Raspberry Pi (via Bash)
```
pip install virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd app && flask run
```