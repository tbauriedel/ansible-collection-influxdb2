#!/usr/bin/python3
# pylint: disable=missing-module-docstring

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tbauriedel.influxdb.plugins.module_utils.utils import (Influx2Api) # pylint: disable=import-error

def run_module():
    '''
    Module to manage InfluxDB buckets
    '''

    # Define new Module with arguments
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            state=dict(type=str, required=True),
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
        rc=""
    )

    # Prepare API class
    API = Influx2Api(module.params['token'], module.params['host']) # pylint: disable=invalid-name

    # Get state of current bucket
    org_id = API.get_orgid_by_name(module.params['org'])
    if org_id == "not found":
        module.exit_json(
            failed=True,
            stderr="No org id found for given org name"
        )

    # Get state of bucket ('present' or 'absent')
    bucket_state = API.get_bucket_status(module.params['name'], org_id)

    # Create bucket if not 'present' but 'present' in configuration
    if module.params['state'] == 'present' and bucket_state == 'absent':
        result['debug'] = "Create bucket"

        rc, content = API.create_bucket(module.params['name'], org_id, module.params['retention'])
        result['rc'] = rc
        if rc != 201:
            module.exit_json(
                failed=True,
                stderr=content
            )

        result['changed'] = True

    # Delete bucket if 'present' but 'absent' in configuration
    elif module.params['state'] == 'absent' and bucket_state == 'present':
        result['debug'] = "Delete bucket"

        rc, content = API.delete_bucket(module.params['name'], module.params['org'])
        result['rc'] = rc
        if rc != 204:
            module.exit_json(
                failed=True,
                stderr=content
            )

        result['changed'] = True

    else:
        result['debug'] = "Keep state of bucket"

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
