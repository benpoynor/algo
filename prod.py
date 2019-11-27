from settings.keys import CoinbaseKeys
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import settings.keys as k


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, key: k.keyset):
        self.api_key = key.public
        self.secret_key = key.private
        self.passphrase = key.passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


class LiveDemo:
    # houses a method that will:
    # check that we can connect and read data from the live account
    # check that we can trade on a sandbox account
    @staticmethod
    def run():
        api_url = 'https://api.pro.coinbase.com/'
        auth = CoinbaseExchangeAuth(CoinbaseKeys.live_test)
        r = requests.get(api_url + 'accounts', auth=auth)
        print(r.json())


class Production:
    def __init__(self):
        self.api_public_key = None
        self.api_private_key = None

    def run(self):
        # start live trading with an algo
        pass
