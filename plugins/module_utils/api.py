# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0


from influxdb_client import InfluxDBClient

class Api():
    def new_client(host, token, timeout=10000) -> InfluxDBClient:
        return InfluxDBClient(host, token, timeout=timeout)
