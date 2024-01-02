#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tbauriedel.influxdb.plugins.module_utils.utils import (
    InfluxApi
)

def run_module():
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

    # Get state of current bucket
    orgID = InfluxApi.get_orgID_by_name(module)
    if orgID == "not found":
        module.exit_json(dict(
            failed=True,
            stderr="No orgID found for given org name"
        ))

    # Get state of bucket ('present' or 'absent')
    bucketState = InfluxApi.get_bucket_status(module)

    # Create bucket if not 'present' but 'present' in configuration
    if module.params['state'] == 'present' and bucketState == 'absent':
        result['debug'] = "Create bucket"

        rc, content = InfluxApi.create_bucket(module)
        result['rc'] = rc
        if rc != 201:
            module.exit_json(
                failed=True,
                stderr=content
            )
            
        result['changed'] = True

    # Delete bucket if 'present' but 'absent' in configuration
    elif module.params['state'] == 'absent' and bucketState == 'present':
        result['debug'] = "Delete bucket"

        rc, content = InfluxApi.delete_bucket(module)
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
    
def main():
    run_module()

if __name__ == '__main__':
    main()