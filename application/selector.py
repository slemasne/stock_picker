import pyEX as p
import random
import pandas as pd

columns = ["beta","dividendYield","day200MovingAvg","marketcap","ytdChangePercent"]

class stockSelector():

    def __init__(self, count, columns):
        self.count = count
        self.columns = columns

    def random_symbols(self):
        symbols = p.symbolsDF()
        symbols = symbols.loc[symbols['type'] == "cs"]
        symbols = [i for i in (p.symbolsDF()["symbol"])]
        return random.sample(symbols, self.count)

    def stock_stats(self):
        stats_list = [{stock :(list((p.stockStats(stock)[k]) for k in self.columns if k in p.stockStats(stock)))} for stock in self.random_symbols()]
        stats_dict = {key :value for dict_ in stats_list for key, value in dict_.items()}
        df_stock_stats = pd.DataFrame.from_dict(stats_dict, orient = "index", columns = columns)
        return df_stock_stats
