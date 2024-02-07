#!/usr/bin/python3
# pylint: disable=missing-module-docstring

from ansible.module_utils.basic import (
    AnsibleModule,
)

from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_organization import (
    Org
)

def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type=str, required=True),
            state=dict(type=str, required=True),
            desc=dict(type=str, required=False),
            host=dict(type=str, required=True),
            token=dict(type=str, required=True)
        )
    )

    result=dict(
        changed=False,
        failed=False,
    )

    if module.params['state'] != 'absent' and module.params['state'] != 'present':
        result['stderr'] = "Invalid state given. Please use 'absent' or 'present'"
        result['failed'] = True

        module.exit_json(**result)


    org = Org(
        result=result,
        host=module.params['host'],
        token=module.params['token'],
        desc=module.params['desc'],
        name=module.params['name'],
        state=module.params['state'],
    )
    
    result = org.return_result()

    module.exit_json(**result)

if __name__ == "__main__":
    run_module()