# twincat-ads-to-ca-bridge
ads-async-based ADS server which can serve EPICS PV data

* Install ads-async
* Run `pv_server` on a machine that has access to PVs
* Add route to TwinCAT PLC to the above machine
* Look at sample TwinCAT code
* Write code to query the Python server for CA data (metadata + value) with the given structures
