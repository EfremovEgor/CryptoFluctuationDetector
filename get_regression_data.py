import requests
import csv
import os

URL = "https://api.binance.com/api/v3/klines"
dataset: list[dict] = list()
btc_response = requests.get(URL + "?symbol=BTCUSDT&interval=1d").json()
eth_response = requests.get(URL + "?symbol=ETHUSDT&interval=1d").json()
for btc_data, eth_data in zip(btc_response, eth_response):
    dataset.append(
        {
            "BTCUSDT": btc_data[4],
            "ETHUSDT": eth_data[4],
        }
    )
with open(os.path.join(os.getcwd(), "data", "dataset.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=("BTCUSDT", "ETHUSDT"))
    writer.writeheader()
    writer.writerows(dataset)
