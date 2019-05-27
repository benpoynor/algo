import random


def fake_data(length):
    fakedata = {
        'open': [],
        'close': [],
        'low': [],
        'high': [],
        'volume': []
    }

    for i in range(length):
        r_open = random.randint(7000, 7100)
        r_close = random.randint(7000, 7100)
        r_high = random.randint(r_open + 1, r_open + 100)
        r_low = random.randint(r_close - 100, r_close- 1)
        fakedata['open'].append(r_open)
        fakedata['high'].append(r_high)
        fakedata['close'].append(r_close)
        fakedata['low'].append(r_low)
        fakedata['volume'].append(random.randint(1, 1000))

    return fakedata
