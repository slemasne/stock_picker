import requests
import pandas as pd

url = r"https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"

class loadData():

    def __init__ (self, sector, source):

        """
        Returns stock market data

        :param sector: the company sector (eg Financials)
        :param source: source of the data for these sector look-ups

        """

        self.sector = sector
        self.source = source

    def __sector_tickers(self):

        """
        Returns a list of individual tickers from the S&P constituents file. 

        """

        snp_file = pd.read_csv(self.source)
        snp_sector = snp_file.query("Sector == '{}'".format(self.sector))
        snp_sector_symbols = [i for i in (snp_sector["Symbol"])]
        return snp_sector_symbols

    def __all_tickers(self):

        """
        Pass the individual tickers from S&P file to get a new list of all S&P tickers + their peers. 

        """

        tickers_collection = self.__sector_tickers()
        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=peers'.format(",".join(tickers_collection))
        peers_data_json = requests.get(url).json()
        peers_dict_keys = list(peers_data_json.keys())
        peers_dict_values = [item for sublist in [peers_data_json.get(i).get("peers") for i in peers_data_json.keys()] for item in sublist]
        unique_tickers = list(set(peers_dict_keys + peers_dict_values))
        return unique_tickers

    def __stock_stats(self):

        """
        Return a DataFrame with three sets of information for each ticker: (1) Stats, (2) Stock Quote, (3) Company Description
        """


        all_tickers = self.__all_tickers()

        url = r'https://api.iextrading.com/1.0/stock/market/batch?symbols={}&types=stats,company,quote'.format(
            ",".join(all_tickers))

        request_json = requests.get(url).json()
        stock_stats_df = pd.DataFrame([request_json[ticker]["stats"] for ticker in request_json]).set_index("symbol")
        company_stats_df = pd.DataFrame([request_json[ticker]["company"] for ticker in request_json]).set_index("symbol")
        price_df = pd.DataFrame([request_json[ticker]["quote"] for ticker in request_json]).set_index("symbol")
        return company_stats_df.merge(stock_stats_df,on='symbol').merge(price_df,on='symbol')

    def formatted_stock_stats(self):

        """
        Returns a formatted DataFrame of ticker data.
        """

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


def stockSelector(risk, sector, strategy, count):

    """
    Returns a list of tickers per strategy defined by user

    :param risk: risk level required
    :param sector: sector required
    :param strategy: strategy required
    :param count: number of results requested 

    """


    data = loadData(sector, url).formatted_stock_stats()
    risk_filtered_data = data[data["betaQuartiles"] == risk]

    if strategy == "Value":
        risk_filtered_data['peRatioQuartiles'] = pd.qcut(risk_filtered_data["peRatio"], 4, labels=False, duplicates="drop")
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["peRatioQuartiles"] == risk_filtered_data["peRatioQuartiles"].min()]

    elif strategy == "Income":
        risk_filtered_data['dividendQuartiles'] = pd.qcut(risk_filtered_data["dividendYield"], 4, labels=False, duplicates="drop")
        strategy_filtered_data = risk_filtered_data[risk_filtered_data["dividendQuartiles"] == risk_filtered_data["dividendQuartiles"].max()]

    return strategy_filtered_data.sample(count)



