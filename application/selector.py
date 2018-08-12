import pyEX as p
import random
import pandas as pd
import requests

columns = ["beta","dividendYield","day200MovingAvg","marketcap","ytdChangePercent"]
url = r"https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"

class stockStats():

    def __init__(self, symbols, columns):
        self.symbols = symbols
        self.columns = columns

    def stock_stats(self):
        stats_list = [{stock :(list((p.stockStats(stock)[k]) for k in self.columns if k in p.stockStats(stock)))} for stock in self.symbols]
        stats_dict = {key :value for dict_ in stats_list for key, value in dict_.items()}
        df_stock_stats = pd.DataFrame.from_dict(stats_dict, orient = "index", columns = columns)
        return df_stock_stats

class loadData():

    def __init__ (self, source):
        self.source = source

    def random_symbols(self, sector, count):
        data = pd.read_csv(self.source)
        data = data.query("Sector == '{}'".format(sector))
        symbols = [i for i in (data["Symbol"])]
        return random.sample(symbols, count)

class returnJSON():

    def __init__(self, symbol_list):
        self.symbol_list = symbol_list

    def return_json(self):
        symbols = ",".join(self.symbol_list)
        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=company,stats'.format(symbols)
        data = requests.get(url)
        data = data.json()
        return data

    def return_data_point(self):
        results = self.return_json()
        return_data_point = results[list(results.keys())[0]]["company"]["companyName"]



data = loadData(url).random_symbols("Financials",3)

results = returnJSON(data).return_json()

company_name = results[list(results.keys())[0]]["company"]["companyName"]
description = results[list(results.keys())[0]]["company"]["description"]
ceo = results[list(results.keys())[0]]["company"]["CEO"]

print (company_name, description, ceo)