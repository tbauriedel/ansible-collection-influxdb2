# influxdb.influxdb2

## Description

With that role you can install and configure InfluxDBv2.
At the moment the configuration is very basic. Over time, this role will be expanded.

## Variables

**Configuration:**
* `influxdb_influxdb2_bolt_path`: InfluxDB bolt-path
* `influxdb_influxdb2_engine_path`: InfluxDB engine-path
* `influxdb_influxdb2_extra_config`: Some extra configuration

**Setup:**
* `influxdb_influxdb2_host`: HTTP address of InfluxDB (default: 'http://localhost:8086')
* `influxdb_influxdb2_primary_user.name`: Username for primary administrative user (default: 'admin')
* `influxdb_influxdb2_primary_user.password`: Password for primary administrative user (default: 'ChangeMe123!')
* `influxdb_influxdb2_primary_org`: Primary organization (default: 'default')
* `influxdb_influxdb2_primary_bucket`: Primary bucket (default: 'default')
* `influxdb_influxdb2_retention`: Retention for primary bucket (default: '0')
* `influxdb_influxdb2_admin_token`: Admin API token created in the setup (default: 'Random123ChangeMe!')

**Organizations**
* `influxdb_influxdb2_orgs`: List of organizations to manage
  * `name`: Name of the organization
  * `state`: State ('present' or 'absent')
  * `desc`: Description
  * `token`: API token to manage the organization

**Buckets**
* `influxdb_influxdb2_buckets`: List of buckets to manage
  * `name`: Name of bucket. ([Bucket naming restrictions!](https://docs.influxdata.com/influxdb/v2/admin/buckets/create-bucket/?t=InfluxDB+API#bucket-naming-restrictions))
  * `state`: State of the bucket ('present' or 'absent')
  * `desc`: Description
  * `org`: InfluxDB organization name
  * `token`: API token to manage the bucket
  * `retention`: Dict of retention rules containing a single object with the following fields
    * `type`: expire
    * `everySeconds`: Number of seconds to retain data (0 means forever)
    * `shardGroupDurationSeconds`: Number of seconds to retain shard groups (**Caution**: The [default values](https://docs.influxdata.com/influxdb/v2/reference/internals/shards/#shard-group-duration) also correspond to the necessary minimum!)

Defaults can be viewed in vars/defaults.yml

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