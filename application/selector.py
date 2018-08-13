import requests
import pandas as pd

url = r"https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"

class loadData():

    def __init__ (self, sector, source):
        self.sector = sector
        self.source = source

    def __collect_tickers(self):
        data = pd.read_csv(self.source)
        data = data.query("Sector == '{}'".format(self.sector))
        symbols = [i for i in (data["Symbol"])]
        return symbols

    def __return_tickers(self):
        tickers_collection = self.__collect_tickers()
        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=peers'.format \
            (",".join(tickers_collection))
        peers_data = requests.get(url)
        peers_data_json = peers_data.json()
        peers_dict_keys = list(peers_data_json.keys())
        peers_dict_values = [item for sublist in [peers_data_json.get(i).get("peers") for i in peers_data_json.keys()] for item in sublist]
        unique_tickers = list(set(peers_dict_keys + peers_dict_values))
        return unique_tickers

    def __stock_stats(self):
        all_tickers = self.__return_tickers()
        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=stats'.format(",".join(all_tickers))
        stock_stats = requests.get(url)
        stock_stats_json = stock_stats.json()
        formatted_dict = [stock_stats_json[ticker]["stats"] for ticker in stock_stats_json]
        stock_stats_df = pd.DataFrame(formatted_dict).set_index("symbol")
        return stock_stats_df

    def formatted_stock_stats(self):
        stock_stats_df = self.__stock_stats()
        stock_stats_df = stock_stats_df[["companyName" ,"marketcap" ,"beta",
                                         "dividendYield" ,"returnOnEquity" ,"peRatioHigh" ,"peRatioLow"]]

        stock_stats_df["beta"] = round(stock_stats_df["beta"],2)
        stock_stats_df["dividendYield"] = round(stock_stats_df["dividendYield"], 2)
        stock_stats_df["peRatio"] = round(((stock_stats_df["peRatioHigh"] + stock_stats_df["peRatioLow"]) / 2),2)

        stock_stats_df["averageBeta"] = round(stock_stats_df["beta"].mean(),2)
        stock_stats_df["averageDividendYield"] = round(stock_stats_df["dividendYield"].mean(),2)
        stock_stats_df["averagePE"] = round(stock_stats_df["peRatio"].mean(), 2)

        stock_stats_df['betaQuartiles'] = pd.qcut(stock_stats_df["beta"], 4 ,labels=False, duplicates = "drop")
        stock_stats_df['dividendQuartiles'] = pd.qcut(stock_stats_df["dividendYield"], 4, labels=False, duplicates="drop")
        stock_stats_df['peRatioQuartiles'] = pd.qcut(stock_stats_df["peRatio"], 4 ,labels=False, duplicates = "drop")

        return stock_stats_df


def stockSelector(risk, sector, strategy, count):
    data = loadData(sector, url).formatted_stock_stats()
    risk_filtered_data = data[data["betaQuartiles"] == risk]

    if strategy == "Value":
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["peRatioQuartiles"] == 0]

    elif strategy == "Income":
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["dividendQuartiles"] == 3]

    try:
        return strategy_filtered_data.sample(count)

    except ValueError:
        print("Unfortunately we have no results available, please try lower your search request")



test =  loadData("Financials", url).formatted_stock_stats()

test2 = stockSelector(0,  "Materials", "Income", 2)

print (test2)