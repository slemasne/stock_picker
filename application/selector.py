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
        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=stats,company,quote'.format(
            ",".join(all_tickers))
        request_data = requests.get(url)
        request_json = request_data.json()

        stock_stats_dict = [request_json[ticker]["stats"] for ticker in request_json]
        stock_stats_df = pd.DataFrame(stock_stats_dict).set_index("symbol")

        company_stats_dict = [request_json[ticker]["company"] for ticker in request_json]
        company_stats_df = pd.DataFrame(company_stats_dict).set_index("symbol")

        price_dict = [request_json[ticker]["quote"] for ticker in request_json]
        price_df = pd.DataFrame(price_dict).set_index("symbol")

        #return pd.merge([company_stats_df, stock_stats_df, price_df])
        return company_stats_df.merge(stock_stats_df,on='symbol').merge(price_df,on='symbol')

    def formatted_stock_stats(self):
        stock_stats_df = self.__stock_stats()

        stock_stats_df["beta"] = round(stock_stats_df["beta"],2)
        stock_stats_df["dividendYield"] = round(stock_stats_df["dividendYield"], 2)
        stock_stats_df["peRatio"] = round(((stock_stats_df["peRatioHigh"] + stock_stats_df["peRatioLow"]) / 2),2)

        stock_stats_df["averageBeta"] = round(stock_stats_df["beta"].mean(),2)
        stock_stats_df["averageDividendYield"] = round(stock_stats_df["dividendYield"].mean(),2)
        stock_stats_df["averagePE"] = round(stock_stats_df["peRatio"].mean(), 2)

        stock_stats_df['betaQuartiles'] = pd.qcut(stock_stats_df["beta"], 4 ,labels=False, duplicates = "drop")

        stock_stats_df = stock_stats_df[~(stock_stats_df[['beta', 'dividendYield', 'peRatio']] == 0).any(axis=1)]


        stock_stats_df = stock_stats_df[["companyName" ,"marketcap", "beta", "averageBeta",
                                         "dividendYield", "averageDividendYield", "peRatio",
                                         "averagePE", "betaQuartiles","returnOnEquity","description","close"]]
        return stock_stats_df

    def stock_stats_for_webpage(self):
        stock_stats_for_webpage = self.formatted_stock_stats()
        stock_stats_for_webpage = stock_stats_for_webpage.drop(columns=['betaQuartiles','description'])
        return stock_stats_for_webpage


def stockSelector(risk, sector, strategy, count):
    data = loadData(sector, url).formatted_stock_stats()
    risk_filtered_data = data[data["betaQuartiles"] == risk]

    if strategy == "Value":
        risk_filtered_data['peRatioQuartiles'] = pd.qcut(risk_filtered_data["peRatio"], 4, labels=False, duplicates="drop")
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["peRatioQuartiles"] == risk_filtered_data["peRatioQuartiles"].min()]

    elif strategy == "Income":
        risk_filtered_data['dividendQuartiles'] = pd.qcut(risk_filtered_data["dividendYield"], 4, labels=False, duplicates="drop")
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["dividendQuartiles"] == risk_filtered_data["dividendQuartiles"].max()]

    return strategy_filtered_data.sample(count)



# Testing
#data = loadData("Financials",url)
#print(data.formatted_stock_stats()["peRatio"]["NYCB"])


