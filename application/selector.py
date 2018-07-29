import pyEX as p
import random
import pandas as pd

def random_symbol(count = 3):
    symbols = p.symbolsDF()
    symbols = symbols.loc[symbols['type'] == "cs"]
    symbols = [i for i in (p.symbolsDF()["symbol"])]
    return random.sample(symbols, count)

symbols = random_symbol()

def stock_beta(symbols_list):
    betas = [{stock: p.stockStats(stock)["beta"]} for stock in symbols_list]
    sorted_betas = sorted(betas, key=lambda x: list(x.values())[0])
    return sorted_betas

beta_list =  stock_beta(symbols)

print (beta_list)