![Lint](https://github.com/tbauriedel/ansible-collection-influxdb2/actions/workflows/yamllint.yml/badge.svg) ![Build](https://github.com/tbauriedel/ansible-collection-influxdb2/actions/workflows/molecule.yml/badge.svg)

> **Note:** Collection is not production-ready yet

# ansible-collection-influxdb2

Ansible collection to manage [InfluxDBv2](https://www.influxdata.com/) repository and setup.  
Read more about InfluxDBv2 in the [official documentation](https://docs.influxdata.com/influxdb/v2/).

The collection is still at a very experimental stage and is growing bit by bit according to my use cases. New configuration options will be implemented when they are needed. If you already have requests, please let me know via issue (or pull request).

It was created with the aim of refreshing my Ansible knowledge and getting in touch with Collections. Any hints for improvements are therefore welcome.

## Roles

* [Role: repos](roles/repos/README.md) - Install the official InfluxDb repositories
* [Role: influxdb2](roles/influxdb2/README.md) - Install and configure InfluxDBv2

## Modules

* [Module: influxdb2_organization](doc/modules/influxdb2_organization.py): Create, update and delete InfluxDBv2 organizations
* [Module: influxdb2_bucket](doc/modules/influxdb2_bucket.md.py): Create, update and delete InfluxDBv2 buckets

## Example

```
- name: InfluxDB
  hosts: all

  vars:
    influxdb_influxdb2_admin_token: 123456789abc!
    influxdb_influxdb2_orgs:
      - name: org1
        desc: "This is a description"
        token: "{{ influxdb_influxdb2_admin_token }}"

    influxdb_influxdb2_buckets:
      - name: bucket-1
        desc: "This is a description"
        org: org1
        token: "{{ influxdb_influxdb2_admin_token }}"
        retention:
          type: 'expire'
          everySeconds: '60000'
          shardGroupDurationSeconds: '7600'

  collections:
    - tbauriedel.influxdb2

  roles:
    - repos
    - influxdb2
```

## Supported systems
| Distribution | Tested on    |
|--------------|--------------|
| Ubuntu       | 22.04        |
| Rocky        | 9            |
