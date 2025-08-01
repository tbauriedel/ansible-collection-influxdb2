# !/usr/bin/python3

# Copyright (c) 2025, Tobias Bauriedel <tobias@bauriedel.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

from ansible.module_utils.basic import (
    AnsibleModule
)

from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_auth import (
    AuthApi
)

DOCUMENTATION = r'''
---
module: influxdb2_auth
short_description: Manage InfluxDB 2.x API tokens
author: "Tobias Bauriedel (@tbauriedel)"
description:
  - Create or delete authorization tokens in InfluxDB 2.x.
  - Token permissions are compared on update. If changed, the token is deleted and recreated.
  - This will result in a changed token string.
options:
  name:
    description:
      - Logical name/description for the token (used as `description` field in InfluxDB).
    required: true
    type: str
  org:
    description:
      - Name of the InfluxDB organization.
    required: true
    type: str
  state:
    description:
      - Desired state of the token.
    choices: [ present, absent ]
    default: present
    type: str
  desc:
    description:
      - Optional description for the token.
    required: false
    type: str
  host:
    description:
      - URL to the InfluxDB server (e.g. https://influxdb.example.com:8086).
    required: true
    type: str
  token:
    description:
      - Token with administrative permissions to manage other tokens.
    required: true
    type: str
    no_log: true
  permissions:
    description:
      - List of resource permissions to assign to the token.
      - Structure:
        - A list of resources (e.g., C(buckets), C(dashboards), C(variables)) and their associated actions.
      - For example:
        - C({ buckets: [ { action: read, bucket: my-bucket } ] })
        - C({ dashboards: [ { action: write } ] })
    required: true
    type: list
  verify_ssl:
    description:
      - Whether to verify the InfluxDB SSL certificate.
    required: false
    type: bool
    default: true
notes:
  - Changing permissions deletes and recreates the token.
  - This means the token string will change.
see also:
  - name: InfluxDB Authorization API
    description: InfluxDB API documentation for managing tokens
'''

EXAMPLES = r'''
- name: Create an API token with bucket and dashboard access
  tbauriedel.influxdb2.influxdb2_auth:
    name: "my-token"
    state: present
    org: default
    host: "https://influxdb.local:8086"
    token: "{{ admin_token }}"
    verify_ssl: false
    permissions:
      - buckets:
          - action: read
            bucket: my-bucket
      - dashboards:
          - action: read
          - action: write

- name: Delete a token
  tbauriedel.influxdb2.influxdb2_auth:
    name: "my-token"
    state: absent
    org: default
    host: "https://influxdb.local:8086"
    token: "{{ admin_token }}"
'''

RETURN = r'''
token:
  description: The token string created or matched.
  type: str
  returned: when state=present
  sample: "my-generated-token-string=="
changed:
  description: Whether a change was made.
  type: bool
  returned: always
msg:
  description: Human-readable status message.
  type: str
  returned: always
'''


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            org=dict(type=str, required=True),
            state=dict(type=str, required=False),
            desc=dict(type=str, required=False),
            host=dict(type=str, required=True),
            token=dict(type=str, required=True, no_log=True),
            permissions=dict(type=list, required=True),
            verify_ssl=dict(type=bool, required=False),
        )
    )

    #module.debug("help")

    result = dict(
        changed=False,
        failed=False,
    )

    if module.params['state'] != 'absent' and module.params['state'] != 'present':
        result['stderr'] = "Invalid state given. Please use 'absent' or 'present'"
        result['failed'] = True

        module.exit_json(**result)

    auth = AuthApi(
        host=module.params['host'],
        token=module.params['token'],
        name=module.params['name'],
        org=module.params['org'],
        state=module.params['state'],
        desc=module.params['desc'],
        permissions=module.params['permissions'],
        verify_ssl=module.params['verify_ssl']
    )

    auth.handle()

    result = auth.return_result()

    module.exit_json(**result)

if __name__ == "__main__":
    run_module()
