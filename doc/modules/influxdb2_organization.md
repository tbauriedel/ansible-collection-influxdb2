# Ansible module: influxdb2_organization

This module creates, updates and deletes organizations from your InfluxDB2.

## Requirements

As this module uses the InfluxDB2 API you will need to install the InfluxDB2 Python3 library.

`pip3 install influxdb-client`

## Module arguments

* `name`: Organization name
* `state`: State of the organization ('present' or 'absent')
* `desc`: Description
* `token`: API token to manage the organization
* `host`: InfluxDB API Endpoint

## Example usage

```
- name: Manage organization
  tbauriedel.influxdb2.influxdb2_organization:
    name: "Example"
    state: present
    desc: "This is a organization"
    token: "{{ influxdb_api_token }}"
    host: "{{ http://localhost:8086 }}"
```
