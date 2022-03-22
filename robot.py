import asyncio
import websockets

import pandas as pd

from json import loads

from bot_utils import set_dataframe


async def bot(pair:str, database:pd.DataFrame):

    websocket = f"wss://stream.binance.com:9443/stream?streams={pair}@trade"

    stream = websockets.connect(websocket)

    async with stream as request_btc:
        data_btc = await request_btc.recv()
        _data = set_dataframe(loads(data_btc)["data"])
        database.append(_data)
        database = database.append(set_dataframe(loads(data_btc)["data"]))

        for pair in database.loc[:,"symbol"]:
            pairs_table = database.loc[database.loc[:, "symbol"] == pair,:]
            if len(pairs_table) >= 5:
                database.loc[pairs_table.index, "MA 5"] = pairs_table.Price.rolling(5).mean()


        return database

async def main():

    database = pd.DataFrame(columns=["symbol", "Price", "Quantity"])

    while True:
        for new_row in asyncio.as_completed({bot("btcusdt", database), bot("ethusdt", database)}):
            database = await new_row
        
        print(database)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
