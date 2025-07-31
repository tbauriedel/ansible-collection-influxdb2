# Ansible module: influxdb2_auth

This module creates, updates and deletes access tokens from your InfluxDB2.

## Requirements

As this module uses the InfluxDB2 API you will need to install the InfluxDB2 Python3 library.

`pip3 install influxdb-client`

## Module arguments
* `name`: Name of token. Only used inside of the module to identify the token (saved in description)
* `state`: State of the token ('present' or 'absent')
* `desc`: Description (Only use in case you dont want to manage the token again after creation. Is used to identify it again)
* `org`: Organization name
* `token`: API token to manage the token
* `verify_ssl`: Verify ssl certificates (Default: `true`)
* `host`: InfluxDB Host to use in API call
* `permissions`: **List** of permissions. An example can be found below.

```yaml
permissions:
  - buckets: # resource
      - action: read # action
        bucket: my-bucket # bucket name (only needed for the bucket resource)
  - dashboards:
      - action: read
  - variables:
      - action: read
      - action: write
  - ...
```

Supported resources:  
- buckets (requires 'action' and 'bucket' name), dashboards, variables, tasks, checks, notifications, orgs, authorizations, labels, secrets, views, documents

Supported actions:  
- read, write

> Note!
> If an existing token’s permissions differ from the desired state, the module deletes and recreates the token under the hood.
> This causes the actual token string to change. Plan accordingly if you store tokens externally or pass them to applications.

## Example usage

```
- name: Manage auth tokens
  tbauriedel.influxdb2.influxdb2_auth:
    name: "{{ item.name }}"
    state: "{{ item.state | default('present') }}"
    desc: "{{ item.desc | default(omit) }}"
    org: "{{ item.org }}"
    token: "{{ influxdb2_influxdb2_admin_token }}"
    host: "{{ influxdb2_influxdb2_host }}"
    verify_ssl: "{{ item.verify_ssl | default(true) }}"
    permissions: "{{ item.permissions }}"
  loop: "{{ influxdb2_influxdb2_tokens }}"
```
