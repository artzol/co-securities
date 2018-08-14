import pandas as pd

from stocks import monthly_open_close, biggest_profit, busy_days, loss_days


def test_monthly_open_close():
    data = {
        'symbol1': pd.DataFrame({
            'Open': [9.0]*2 + [10.0]*2 + [11.0]*2,
            'Close': [4.0]*2 + [3.0]*2 + [2.0]*2
        }, index=pd.date_range('2017-01-01', periods=6, freq='d'))
    }
    expected = {
        'symbol1': [{'month': '2017-01', 'average_open': '$10.00', 'average_close': '$3.00'}]
    }
    assert monthly_open_close(data) == expected


def test_biggest_profit():
    df = pd.DataFrame.from_dict({
        'Date': pd.date_range('2017-01-01', periods=3, freq='d'),
        'High': [100.0, 100.0, 100.0],
        'Low': [90.0, 20.0, 80.0]
    })
    data = {'symbol': df.set_index('Date')}
    expected = {'symbol': {'Date': '2017-01-02', 'Profit': '$80.00'}}
    assert biggest_profit(data) == expected


def test_busy_days():
    df = pd.DataFrame.from_dict({
        'Date': pd.date_range('2017-01-01', periods=6, freq='d'),
        'Volume': [80.0]*2 + [100.0]*2 + [120.0]*2
    })
    data = {'symbol': df.set_index('Date')}
    expected = {'symbol': {
        'Average_volume': 100.0,
        'Busy_days': [{'Date': '2017-01-05', 'Volume': 120.0}, {'Date': '2017-01-06', 'Volume': 120.0}]
    }}
    assert busy_days(data) == expected


def test_biggest_loser():
    dates = pd.date_range('2017-01-01', periods=4, freq='d')
    # 3 symbols where symbol 1 has 0 loss days, symbol2 - 2 loss days, symbol3 - 3 loss days
    data = {
        'symbol1': pd.DataFrame({
            'Open': [5.0, 5.0, 5.0, 5.0],
            'Close': [6.0, 6.0, 6.0, 6.0]
        }, index=dates),
        'symbol2': pd.DataFrame({
            'Open': [5.0, 5.0, 5.0, 5.0],
            'Close': [4.0, 3.0, 6.0, 6.0]
        }, index=dates),
        'symbol3': pd.DataFrame({
            'Open': [5.0, 5.0, 5.0, 5.0],
            'Close': [4.0, 3.0, 2.0, 6.0]
        }, index=dates)
    }
    expected = {'symbol': 'symbol3', 'days': 3}
    assert loss_days(data) == expected
