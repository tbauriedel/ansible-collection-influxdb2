# Ansible module: influxdb_bucket

This module creates, updates and deletes buckets from your InfluxDB2.

## Requirements

As this module uses the InfluxDB2 API you will need to install the InfluxDB2 Python3 library.

`pip3 install influxdb-client`

## Module arguments

* `name`: Bucket name
* `state`: State of the bucket ('present' or 'absent')
* `org`: Name of the corresponding organization
* `desc`: Description
* `token`: API token to manage the organization
* `host`: InfluxDB API Endpoint
* `retention`: Dict of retention rules containing a single object with the following fields
  * `type`: Retention type
  * `everySeconds`: Number of seconds to retain data (0 means forever)
  * `shardGroupDurationSeconds`: Number of seconds to retain shard groups (**Caution**: The [default values](https://docs.influxdata.com/influxdb/v2/reference/internals/shards/#shard-group-duration) also correspond to the necessary minimum!)

## Example usage

```
- name: Manage bucket
  tbauriedel.influxdb2.influxdb2_bucket:
    name: "Example"
    state: present
    desc: "This is a bucket"
    org: "{{ item.org }}"
    token: "{{ item.token }}"
    host: "{{ influxdb_influxdb2_host }}"
    retention:
      type: "{{ item.retention.type }}" 
      everySeconds: "{{ item.retention.everySeconds }}"
      shardGroupDurationSeconds: "{{ item.retention.shardGroupDurationSeconds) }}"
  loop: "{{ influxdb_influxdb2_buckets }}"
```
