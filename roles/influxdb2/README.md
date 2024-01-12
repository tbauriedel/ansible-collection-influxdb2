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

**Buckets**
* `influxdb_influxdb2_buckets`: List of buckets to manage
  * `name`: Name of bucket. (watch [bucket naming restrictions](https://docs.influxdata.com/influxdb/v2/admin/buckets/create-bucket/?t=InfluxDB+API#bucket-naming-restrictions))
  * `state`: state of bucket ('present' or 'absent')
  * `org`: InfluxDB organization name
  * `token`: API token to manage the bucket
  * `retention`: List of retention rules containing a single object with the following fields
    * `type`: expire
    * `everySeconds`: Number of seconds to retain data (0 means forever)
    * `shardGroupDurationSeconds`: Number of seconds to retain shard groups (0 means forever)

Defaults can be viewed in vars/defaults.yml

## Example

Install the official InfluxDB repository:
```
- hosts: all
  become: true

  roles:
    - influxdb2
```