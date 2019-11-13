# https://docs.gemini.com/rest-api/#introduction
from settings.keys import GeminiKeys


class LiveDemo:
    def __init__(self):
        self.api_public_key = GeminiKeys.demo_public
        self.api_private_key = GeminiKeys.demo_private

    def log_settings(self):
        print('Running tests using... \n'
              ' private (demo) key: {} \n '
              'public (demo) key: {}'
              .format(self.api_private_key, self.api_public_key))

    def test_buy(self):
        # buy from gemini
        pass

    def test_sell(self):
        # sell from gemini
        pass

    def test_run(self):
        self.log_settings()


class Production:
    def __init__(self):
        self.api_public_key = None
        self.api_private_key = None

    def run(self):
        # start live trading with an algo
        pass
