# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias@bauriedel.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# # pylint: disable=missing-module-docstring

from ansible.module_utils.basic import (
    AnsibleModule,
)

from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_organization import (
    OrgApi
)

DOCUMENTATION = r'''
---
module: influxdb2_organization
short_description: Manage InfluxDB 2.x organizations
description:
  - This module allows you to create or delete organizations in InfluxDB 2.x via the HTTP API.
  - Supports setting descriptions for the organizations.
version_added: "1.0.0"
author: "Tobias Bauriedel"
options:
  name:
    description:
      - Name of the organization to manage.
    required: true
    type: str
  state:
    description:
      - Desired state of the organization.
    choices: [present, absent]
    required: true
    type: str
  desc:
    description:
      - Optional description of the organization.
    required: false
    type: str
  host:
    description:
      - The base URL of the InfluxDB 2.x API endpoint.
    required: true
    type: str
  verify_ssl:
    description:
      - Whether to verify TLS certificates.
    required: false
    type: bool
    default: true
  token:
    description:
      - InfluxDB API token used for authentication.
    required: true
    type: str
    no_log: true
'''

EXAMPLES = r'''
- name: Create an InfluxDB organization
  tbauriedel.influxdb2.influxdb2_organization:
    name: example_org
    state: present
    desc: "Development metrics"
    host: https://influxdb.example.com
    verify_ssl: true
    token: "{{ influxdb_token }}"

- name: Delete an InfluxDB organization
  tbauriedel.influxdb2.influxdb2_organization:
    name: old_org
    state: absent
    host: https://influxdb.example.com
    verify_ssl: false
    token: "{{ influxdb_token }}"
'''


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            state=dict(type=str, required=True),
            desc=dict(type=str, required=False),
            host=dict(type=str, required=True),
            verify_ssl=dict(type=bool, required=False),
            token=dict(type=str, required=True, no_log=True),
        )
    )

    result = dict(
        changed=False,
        failed=False,
    )

    if module.params['state'] != 'absent' and module.params['state'] != 'present':
        result['stderr'] = "Invalid state given. Please use 'absent' or 'present'"
        result['failed'] = True

        module.exit_json(**result)

    org = OrgApi(
        result=result,
        host=module.params['host'],
        token=module.params['token'],
        desc=module.params['desc'],
        name=module.params['name'],
        state=module.params['state'],
        verify_ssl=module.params['verify_ssl'],
    )

    org.handle()

    result = org.return_result()

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
