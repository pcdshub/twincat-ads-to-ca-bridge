import asyncio
import functools
import logging

import epics
from ads_async import constants, log, symbols
from ads_async.asyncio.server import AsyncioServer

logger = logging.getLogger(__name__)


def _update_callback(sym, pvname, value, **kwargs):
    print("Update", pvname, value)
    sym.write(int(value * 10))


async def run_pv_server(pv_dictionary):

    database = symbols.SimpleDatabase()

    sym = database.add_basic_symbol(
        name="random_walk:x",
        data_type=constants.AdsDataType.INT16,
        comment="A first symbol",
    )

    database.add_basic_symbol(
        name="random_walk:dt",
        data_type=constants.AdsDataType.INT16,
        comment="A second symbol",
    )

    for sym in database.data_area.symbols.values():
        pv = epics.PV(sym.name)
        pv.add_callback(functools.partial(_update_callback, sym))

    server = AsyncioServer(database)
    await server.start()
    await server.serve_forever()


if __name__ == "__main__":
    log.configure(level="DEBUG")
    asyncio.run(run_pv_server({}), debug=True)
