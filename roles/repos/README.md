# influxdb.repos

## Description

With that role the official [InfluxDB repository](https://repos.influxdata.com) and signing key will be installed.

## Variables

Defaults can be viewed in vars/defaults.yml

## Example

Install the official InfluxDB repository:
```
- hosts: all
  become: true

  roles:
    - repos
```