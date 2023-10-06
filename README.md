## Overview

These files are provided for reference only, as the supporting AWS infrastructure is not expected to be available.

The simulator can be run locally; its connection to an MQTT broker has been disabled.

### Simulator

```bash
pip install pipenv
pipenv install
cd simulator
python sim.py --sensors 10 --interval 60
```
