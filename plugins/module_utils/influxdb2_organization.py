# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

from typing import List
from influxdb_client import Organization
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.api import (
    Api
)


class OrgApi():
    def __init__(self, host, token, name='', state='', desc='', result=dict):
        self.name = name
        self.state = state
        self.desc = desc
        self.result = result

        self.client = Api.new_client(
            host=host, token=token).organizations_api()

    def return_result(self) -> dict:
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

        self.delete(org.id)
        self.result['changed'] = True
        self.result['msg'] = self.name + " has been deleted"

        return

    def handle_present(self):
        # build emtpy org
        pre_org = Organization(
            name=self.name, description=self.desc, status='inactive')

        # fetch all orgs and save found bucket into pre_org
        for row in self.get_all():
            if row.name != self.name:
                continue
            pre_org = self.get_by_id(row.id)
            break

        if pre_org.status != 'active':
            res = self.create()
            self.result['changed'] = True
            self.result['msg'] = self.name + " has been created"
            return

        if (
            (pre_org.description or "") != self.desc or
            self.name != pre_org.name
        ):
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

    def get_all(self) -> List[Organization]:
        return self.client.find_organizations()

    def get_by_id(self, id) -> Organization:
        return self.client.find_organization(org_id=id)

    def get_by_name(self, name) -> Organization:
        for row in self.get_all():
            if row.name != name:
                continue
            return row
        return Organization(name='', status='inactive')
