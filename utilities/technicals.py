
class Technicals:

    @staticmethod
    def sma(period, dataset, index):
        ma = 0
        for i in range(period):
            if index - i > 0:
                ma += float(dataset[index - i]['close'])
            else:
                return 0
        return ma / period
