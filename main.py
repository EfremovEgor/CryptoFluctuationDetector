import asyncio
import aiohttp

MAX_REQUESTS_PER_SECOND = 5
REQUEST_COUNT = 2
SLEEP_TIME = 1 / int(MAX_REQUESTS_PER_SECOND / REQUEST_COUNT)
print("-------------- SLEEP TIME:", SLEEP_TIME, "--------------")
URL = "https://api.binance.com/api/v3/avgPrice"
PING_URL = "https://api.binance.com/api/v3/ping"
FUTURES = ["BTCUSDT", "ETHUSDT"]


async def get_data(session: aiohttp.ClientSession, future: str) -> float:
    async with session.get(url=URL + f"?symbol={future}") as resp:
        data = await resp.json()
    return float(data["price"])


async def ping(session: aiohttp.ClientSession) -> None:
    async with session.get(url=PING_URL) as resp:
        if resp.status != 200:
            print("SERVER DOESN'T RESPOND")
            exit()


async def main() -> None:
    previous_btc_price = None
    previous_eth_price = None
    while True:
        async with aiohttp.ClientSession() as session:
            tasks = list()
            tasks.append(asyncio.ensure_future(ping(session)))
            for future in FUTURES:
                tasks.append(asyncio.ensure_future(get_data(session, future)))
            data = (await asyncio.gather(*tasks))[1:]
            current_btc_price = data[0]
            current_eth_price = data[1]
            if previous_btc_price is not None and previous_eth_price is not None:
                true_eth_deviation = (
                    previous_eth_price / current_eth_price
                    - previous_btc_price / current_btc_price
                )
                print(f"{(true_eth_deviation)*100}%")
            previous_btc_price = current_btc_price
            previous_eth_price = current_eth_price
            await asyncio.sleep(SLEEP_TIME)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("---------------------------------------------")
