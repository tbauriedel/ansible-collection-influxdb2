# influxdb.influxdb

## Description

With that role you can install and configure InfluxDB.
At the moment the configuration is very basic. Over time, this role will be expanded.

## Variables

* `influxdb_influxdb_bolt_path`: InfluxDB bolt-path
* `influxdb_influxdb_engine_path`: InfluxDB engine-path
* `influxdb_influxdb_extra_config`: Extra configuration

Defaults can be viewed in vars/defaults.yml

## Example

Install the official InfluxDB repository:
```
- hosts: all
  become: true

  roles:
    - influxdb
```