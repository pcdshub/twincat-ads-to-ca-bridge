import asyncio
import ctypes
import functools
import logging

import epics
from ads_async import log, symbols
from ads_async.asyncio.server import AsyncioServer


class PvMetadata(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", ctypes.c_double),
        ("status", ctypes.c_int16),
        ("severity", ctypes.c_int16),
        ("data_type", ctypes.c_uint8),
    ]


class PvData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("metadata", PvMetadata),
        ("value", ctypes.c_double),
    ]


logger = logging.getLogger(__name__)


def _update_callback(
    sym: symbols.ComplexSymbol,
    pvname: str,
    value,
    timestamp: float,
    status: int,
    severity: int,
    **kwargs
):
    print("Update", pvname, value)
    data = PvData(
        metadata=PvMetadata(
            timestamp=timestamp or 0.0,
            status=status,
            severity=severity,
            data_type=0,
        ),
        value=float(value),
    )
    sym.write(data)


async def run_pv_server(pv_dictionary):
    database = symbols.SimpleDatabase()

    database.add_complex_symbol(
        name="random_walk:x",
        cls=PvData,
    )

    for sym in database.data_area.symbols.values():
        pv = epics.PV(sym.name, form="time")
        pv.add_callback(functools.partial(_update_callback, sym))

    server = AsyncioServer(database)
    await server.start()
    await server.serve_forever()


if __name__ == "__main__":
    log.configure(level="DEBUG")
    asyncio.run(run_pv_server({}), debug=True)
