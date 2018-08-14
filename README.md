# co-securities

## Installation

Script is written and tested using python 3.6 and python 2.7. 

Install dependencies:
```bash
pip3 install -r requirements.txt
``` 
Replace `pip3` with `pip` if using python 2.7.


## Running script

Before running, script has to be initialized with quandl API key. By default key is read
from file named **api_key**, located in the script's directory.

Run script:
```bash
python3 stocks.py
```
Replace `python3` with `python` if using python 2.7.

## Command line arguments

Script supports following command line parameters:
* `--max-daily-profit` - display maximum profit for each security
* `--busy-day` - display days with high activity for each security
* `--biggest-loser` - display security with highest number of days where closing price was lower than opening price
* `--api-keyfile` - path to file with quandl API key (optional). Defaults to **api_key**

## Testing

Tests use pytest framework https://pytest.org.

Install requirements:
```bash
pip3 install -r requirements.txt
```
Run tests:
```
pytest
```