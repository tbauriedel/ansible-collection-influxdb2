# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias@bauriedel.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-module-docstring

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_bucket import (
    BucketApi
)

DOCUMENTATION = r'''
---
module: influxdb2_bucket
short_description: Manage InfluxDB 2.x buckets
description:
  - This module allows you to create or delete buckets in InfluxDB 2.x using its REST API.
  - Supports setting retention policies and bucket descriptions.
version_added: "1.0.0"
author: "Tobias Bauriedel"
options:
  name:
    description:
      - Name of the bucket to manage.
    required: true
    type: str
  state:
    description:
      - Desired state of the bucket.
    choices: [present, absent]
    required: true
    type: str
  desc:
    description:
      - Description of the bucket.
    required: false
    type: str
  org:
    description:
      - Name of the organization in which the bucket exists.
    required: true
    type: str
  host:
    description:
      - The InfluxDB 2.x API endpoint, e.g., https://influxdb.example.com.
    required: true
    type: str
  verify_ssl:
    description:
      - Whether to verify TLS/SSL certificates.
    type: bool
    required: false
    default: true
  token:
    description:
      - The InfluxDB API token used for authentication.
    required: true
    type: str
    no_log: true
  retention:
    description:
      - Retention policy rules for the bucket.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - The type of retention policy. Typically set to 'expire'.
        type: str
        required: false
      everySeconds:
        description:
          - Duration (in seconds) to retain data. 0 means data is kept forever.
        type: int
        required: false
      shardGroupDurationSeconds:
        description:
          - Duration (in seconds) to retain shard groups. Must match InfluxDB's minimum values.
        type: int
        required: false
'''

EXAMPLES = r'''
- name: Create a bucket with retention policy
  tbauriedel.influxdb2.influxdb2_bucket:
    name: example_bucket
    state: present
    org: example_org
    host: https://influxdb.example.com
    token: "{{ influxdb_token }}"
    desc: "Metrics bucket"
    verify_ssl: true
    retention:
      type: expire
      everySeconds: 604800
      shardGroupDurationSeconds: 86400

- name: Delete a bucket
  tbauriedel.influxdb2.influxdb2_bucket:
    name: old_bucket
    state: absent
    org: example_org
    host: https://influxdb.example.com
    token: "{{ influxdb_token }}"
'''


def run_module():
    '''
    Module to manage InfluxDB buckets
    '''

    # Define new Module with arguments
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            state=dict(type=str, required=True),
            desc=dict(type=str, required=False),
            token=dict(type=str, Required=True, no_log=True),
            host=dict(type=str, Required=True),
            org=dict(type=str, required=False),
            retention=dict(type=dict, required=False),
            verify_ssl=dict(type=bool, required=False),
        )
    )

    if module.params['state'] != 'absent' and module.params['state'] != 'present':
        module.exit_json(
            failed=True,
            stderr="Invalid state provided. Use 'present' or 'absent'"
        )

    # Default result
    result = dict(
        changed=False,
        failed=False,
    )

    bucket = BucketApi(
        result=result,
        name=module.params['name'],
        state=module.params['state'],
        host=module.params['host'],
        token=module.params['token'],
        desc=module.params['desc'],
        org=module.params['org'],
        retention=module.params['retention'],
        verify_ssl=module.params['verify_ssl'],
    )

    bucket.handle()

    result = bucket.return_result()

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
