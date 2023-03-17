import asyncio
import aiohttp
import datetime
from config import *

CURRENT_HOUR_TRUE_SHIFT = None


def get_true_shift(unbound_future_price: float, dependent_future_price: float) -> float:
    return 0.0778 * unbound_future_price - 175.63 - dependent_future_price


async def get_data(future: str, session: aiohttp.ClientSession = None) -> float:
    url = URL + f"?symbol={future}"
    context_manager = (
        session.get(url=url) if session is not None else aiohttp.request("get", url=url)
    )
    async with context_manager as resp:
        data = await resp.json()
    return float(data["price"])


async def server_available(session: aiohttp.ClientSession = None) -> bool:
    context_manager = (
        session.get(url=PING_URL)
        if session is not None
        else aiohttp.request("get", url=PING_URL)
    )
    try:
        async with context_manager as resp:
            return resp.status == 200

    except aiohttp.client_exceptions.ClientConnectorError:
        return False


async def get_current_true_shift():
    async with aiohttp.ClientSession() as session:
        tasks = list()
        tasks.append(asyncio.ensure_future(server_available(session)))
        for future in FUTURES:
            tasks.append(asyncio.ensure_future(get_data(future, session=session)))
        data = await asyncio.gather(*tasks)
        if not data[0]:
            print("[Сервер не отвечает]")
            exit()
        current_true_shift = get_true_shift(*data[1:])
    return current_true_shift


async def main() -> None:
    await asyncio.sleep(1)
    while True:
        current_true_shift = await get_current_true_shift()
        if CURRENT_HOUR_TRUE_SHIFT is None:
            continue
        difference = abs(
            (current_true_shift - CURRENT_HOUR_TRUE_SHIFT) / current_true_shift
        )
        if difference >= DIFFERENCE_THRESHOLD:
            print(
                f"[{datetime.datetime.now()}] Собственное движение цены изменилось на:",
                difference * 100,
                "%",
            )
        await asyncio.sleep(SLEEP_TIME)


async def update():
    print("[Проверка доступности сервера]")
    if not await server_available():
        print("[Сервер не отвечает]")
        exit()
    print("[Сервер доступен]")
    while True:
        global CURRENT_HOUR_TRUE_SHIFT
        CURRENT_HOUR_TRUE_SHIFT = await get_current_true_shift()
        tasks = list()
        tasks.append(asyncio.ensure_future(server_available()))
        for future in FUTURES:
            tasks.append(asyncio.ensure_future(get_data(future)))
        data = (await asyncio.gather(*tasks))[1:]
        print(
            f"[Цены на {datetime.datetime.now()}]\n[BTCUSDT] - {data[0]} \n[ETHUSDT] - {data[1]}"
        )
        await asyncio.sleep(3600)


if __name__ == "__main__":
    print("-------------- Время между запросами:", SLEEP_TIME, "с --------------")
    loop = asyncio.get_event_loop()
    loop.create_task(update())
    loop.create_task(main())
    pending = asyncio.all_tasks(loop=loop)
    group = asyncio.gather(*pending)
    try:
        loop.run_until_complete(group)
    except (KeyboardInterrupt, SystemExit):
        print("----------------------------------------------------------")
