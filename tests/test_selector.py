from application.selector import loadData
from unittest.mock import patch
import pandas as pd
import unittest

url = r"https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"

class loadDataTest(unittest.TestCase):

    def test_collect_tickers(self):
        data = loadData("Financials", url)
        test_collect_tickers = data._loadData__collect_tickers()
        self.assertTrue (isinstance(test_collect_tickers, list))
        self.assertTrue("BLK" in test_collect_tickers)

    @patch.object(loadData, '_loadData__return_tickers', return_value = ["BLK","BAC"])
    def test_stock_stats(self, return_tickers):
        data = loadData("Financials", url)
        df = data.formatted_stock_stats()
        self.assertTrue(isinstance(df, pd.DataFrame))

if __name__ == '__main__':
    unittest.main()




