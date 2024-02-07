# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

from influxdb_client import Organization
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.api import (
    Api
)

class Org():
    def __init__(self, name, state, desc, result, host, token):
        self.name = name
        self.state = state
        self.desc = desc
        self.result = result

        self.client = Api.new_client(host=host, token=token).organizations_api()

        self.handle()

        return

    
    def return_result(self) ->dict:
        return self.result

    
    def handle(self):
        if self.state == 'absent':
            self.handle_absent()
        elif self.state == 'present':
            self.handle_present()

        return

    
    def handle_absent(self):
        org = Organization(name=self.name, status='inactive')
        for row in self.get_all():
            if row.name != self.name:
                continue
            org = row
            break

        if org.status != 'active':
            return

        res = self.delete(org.id)
        self.result['debug'] = res
        self.result['changed'] = True
        self.result['msg'] = self.name + " has been deleted"
        
        return


    def handle_present(self):
        pre_org = Organization(name=self.name, description=self.desc, status='inactive')
        for row in self.get_all():
            if row.name != self.name:
                continue
            pre_org = self.get(row.id)
            break

        if  pre_org.status != 'active':
            res = self.create()
            self.result['changed'] = True
            self.result['msg'] = self.name + " has been created"
            return

        if self.desc != pre_org.description:
            self.update(pre_org.id)
            self.result['changed'] = True
            self.result['msg'] = self.name + " has been updated"
    
        return


    def create(self) -> Organization:
        return self.client.create_organization(name=self.name, organization=Organization(name=self.name, description=self.desc))


    def update(self, id) -> Organization:
        return self.client.update_organization(organization=Organization(name=self.name, description=self.desc, id=id))


    def delete(self, id):
        return self.client.delete_organization(org_id=id)


    def get_all(self) -> list[Organization]:
        return self.client.find_organizations()


    def get(self, id) -> Organization:
        return self.client.find_organization(org_id=id)