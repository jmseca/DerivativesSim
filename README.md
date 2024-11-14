# PMC Simulation Tool

Structured Products Simulator built for the 5-squared competition 1st edition.

## Comment

This was built in Linux. While testing in windows the geometry of the app was a bit too big.
Feel free to change it under src/app/AppRoot.py if needed

Additionally, for some reason that we do not know, if the code is run in macOs, the buttons and inputs
have no background

## Pre-requisites

#### Python Packages

For the simulation to work, python and some python packages need to be installed. Please follow the following rules:

**macOs/Windows**

1. Run
```
pip install -r requirements.txt
```

**Linux**

1. Install `tkinter`:
```
sudo apt update
sudo apt install python3-tk
```
2. Run
```
pip install -r requirements.txt
```

## Run Application

```
cd src/app/
python AppRoot.py
```

