# MealGauge
## Project Description

This project aims to help students avoid long lines at dining halls.
A live camera powered by a Raspberry Pi provides a feed on site.
Our website then displays the data, using computer vision to provide a person count.


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
