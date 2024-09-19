#!/usr/bin/python3
# pylint: disable=missing-module-docstring

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_bucket import (
    BucketApi
)


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
            retention=dict(type=dict, required=False)
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
        retention=module.params['retention']
    )

    bucket.handle()

    result = bucket.return_result()

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
