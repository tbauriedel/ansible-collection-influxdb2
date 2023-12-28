![Lint](https://github.com/tbauriedel/ansible-collection-influxdb/actions/workflows/yamllint.yml/badge.svg)

> **Note:** Collection is work in progress

# ansible-collection-influxdb

Collection to manage InfluxDB repository and setup.

The collection is still at a very experimental stage and is growing bit by bit according to my use cases. New configuration options will be implemented when they are needed. If you already have requests, please let me know via issue (or pull request).

It was created with the aim of refreshing my Ansible knowledge and getting in touch with Collections. Any hints for improvements are therefore welcome.

## Supported systems
| Distribution | Tested on |
|--------------|-----------|
| Ubuntu       | 22.04     |
| Centos       | 9 Stream  |

## Roles

* [Role: repos](roles/repos/README.md) (add repositories)
* [Role: influxdb](roles/influxdb/README.md) (install and configure influxdb)
