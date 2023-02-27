import aiohttp
import asyncio
import time
url = 'https://fapi.binance.com/fapi/v1/ticker/bookTicker?symbol=ETHUSDT'


class BadResponseStatus(Exception):
    """Ошибка при парсинге биржи"""
    pass


async def parsing_binance():
    """Запрос на тикер фьючерсов Binance"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                res = await resp.json()
                return res['bidPrice']
            else:
                raise BadResponseStatus


def check_changes_binance(sleep_time=3600):
    """Подсчёт изменений в процентном соотношении"""
    first_fetch = float(asyncio.run(parsing_binance()))
    print(first_fetch)
    time.sleep(sleep_time)
    second_fetch = float(asyncio.run(parsing_binance()))
    print(second_fetch)
    result = abs(float((second_fetch - first_fetch)/first_fetch)*100)
    if result >= 1:
        return result
    else:
        return 'Курс почти на том же месте'


if __name__ == "__main__":
    while True:
        print(check_changes_binance(sleep_time=3600))
