MAX_REQUESTS_PER_SECOND = 5
REQUEST_COUNT = 2
URL = "https://api.binance.com/api/v3/avgPrice"
PING_URL = "https://api.binance.com/api/v3/ping"
FUTURES = ["BTCUSDT", "ETHUSDT"]
DIFFERENCE_THRESHOLD = 0.01
SLEEP_TIME = 1 / int(MAX_REQUESTS_PER_SECOND / REQUEST_COUNT)
