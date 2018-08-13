# co-securities

## Installation

Script is tested with python 3.6, but it can work with python 2.7 as well. To install,
simply run `pip3 install -r requirements.txt` (preferrably in virtualenv).

## Running script

Before running, script has to be initialized with quandl API key. By default key is read
from file named **api_key**, located in the script's directory.
To run script do:
```
python3 stocks.py
```

## Command line arguments

Script supports following command line parameters:
* `--max-daily-profit`
* `--busy-day`
* `--biggest-loser`
* `--api-keyfile`