![Lint](https://github.com/tbauriedel/ansible-collection-influxdb/actions/workflows/yamllint.yml/badge.svg)

> **Note:** Collection is work in progress

# ansible-collection-influxdb

Ansible collection to manage [InfluxDB](https://www.influxdata.com/) repository and setup.  
Read more about InfluxDB in the [official documentation](https://docs.influxdata.com/influxdb/v2/).

The collection is still at a very experimental stage and is growing bit by bit according to my use cases. New configuration options will be implemented when they are needed. If you already have requests, please let me know via issue (or pull request).

It was created with the aim of refreshing my Ansible knowledge and getting in touch with Collections. Any hints for improvements are therefore welcome.

## Roles

* [Role: repos](roles/repos/README.md) - Install the official InfluxDb repositories
* [Role: influxdb](roles/influxdb/README.md) - Install and configure InfluxDB

## Example

```
- hosts: all
  become: true
  vars:
    influxdb_influxdb_admin_token: 12345678abcdefg
    influxdb_influxdb_buckets:
      - name: foobar1
        state: absent
        org: default
        token: "{{ influxdb_influxdb_admin_token }}"
        host: "{{ influxdb_influxdb_host }}"
        retention:
          type: 'expire'
          everySeconds: '50000'
          shardGroupDurationSeconds: '0'

  collections:
    tbauriedel.influxdb

  roles:
    - repos
    - influxdb
```

## Supported systems
| Distribution | Tested on |
|--------------|-----------|
| Ubuntu       | 22.04     |
| Centos       | 9 Stream  |
