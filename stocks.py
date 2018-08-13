import warnings
import pprint
import argparse

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import quandl


DATE_FROM = '2017-01-01'
DATE_TO = '2017-06-30'


def init_quandl(key_file):
    """
    Initialize quandl api with key from key file
    :param key_file: path to api key file
    """
    with open(key_file, 'r') as f:
        key = f.read()
        quandl.ApiConfig.api_key = key


def download_set(*symbols):
    """
    Download data for given ticker symbols from quandl.
    Returns mapping symbol -> quandl data
    :param symbols: symbols to download
    :return: dictionary symbol -> pandas.DataFrame
    """
    result = {}
    for symbol in symbols:
        dataset = quandl.get('WIKI/{}'.format(symbol), start_date=DATE_FROM, end_date=DATE_TO)
        result[symbol] = dataset
    return result


def monthly_open_close(data_dict):
    """
    Calculate average open and close price for each symbol
    :param data_dict: dictionary of symbol -> data
    :return:
    """
    result = {}
    for symbol, data in data_dict.items():
        monthly_mean = data.resample('M')['Open', 'Close'].mean()
        monthly_mean['month'] = monthly_mean.index.strftime('%Y-%m')
        monthly_mean['average_open'] = monthly_mean['Open'].map('${:,.2f}'.format)
        monthly_mean['average_close'] = monthly_mean['Close'].map('${:,.2f}'.format)
        result[symbol] = monthly_mean[['average_open', 'average_close', 'month']].to_dict('records')
    return result


def biggest_profit(data_dict):
    result = {}
    for symbol, data in data_dict.items():
        result[symbol] = {}
        data['Profit'] = data['High'] - data['Low']
        data['Date'] = data.index.strftime('%Y-%m-%d')
        max_day = data.loc[data['Profit'].idxmax()]
        result[symbol]['Profit'] = '${:,.2f}'.format(max_day['Profit'])
        result[symbol]['Date'] = max_day['Date']
    return result


def busy_days(data_dict):
    result = {}
    for symbol, data in data_dict.items():
        result[symbol] = {}
        volume_mean = data['Volume'].mean()
        result[symbol]['Average_volume'] = volume_mean
        volume_110 = volume_mean * 1.1
        data['Date'] = data.index.strftime('%Y-%m-%d')
        target_days = data.loc[data['Volume'] > volume_110]
        result[symbol]['Busy_days'] = target_days[['Date', 'Volume']].to_dict('records')
    return result


def loss_days(data_dict):
    days_per_ticker = []
    for symbol, data in data_dict.items():
        days = data.loc[data['Close'] < data['Open']]
        days_per_ticker.append((symbol, days.shape[0]))
    min_symbol, min_days = min(days_per_ticker)
    return {
        'symbol': min_symbol,
        'days': min_days
    }


def main(api_keyfile, show_profit=False, show_busy=False, show_loser=False):
    init_quandl(api_keyfile)
    data = download_set('GOOGL', 'MSFT', 'COF')

    processed = monthly_open_close(data)
    pprint.pprint(processed)
    if show_profit:
        p2 = biggest_profit(data)
        pprint.pprint(p2)
    if show_busy:
        r = busy_days(data)
        pprint.pprint(r)
    if show_loser:
        r = loss_days(data)
        pprint.pprint(r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-daily-profit', action='store_true', help='calculate day with maximum profit for each security')
    parser.add_argument('--busy-day', action='store_true', help='display days with high activity')
    parser.add_argument('--biggest-loser', action='store_true', help='display security with most days with close < open')
    parser.add_argument('--api-keyfile', default='api_key', help='location of file with quandl api key')
    args = parser.parse_args()

    main(args.api_keyfile, args.max_daily_profit, args.busy_day, args.biggest_loser)
