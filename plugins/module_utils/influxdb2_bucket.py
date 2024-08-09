# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

from influxdb_client import Bucket ,BucketRetentionRules, Buckets
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.api import (
    Api
)
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_organization import (
    OrgApi
)

class BucketApi():
    def __init__(self, name, state, desc, result, host, token, org, retention):
        self.name = name
        self.state = state
        self.desc = desc
        self.org = org
        self.retention = retention
        self.result = result
        
        self.client = Api.new_client(host=host, token=token).buckets_api()

        self.host = host
        self.token = token

    
    def return_result(self) ->dict:
        return self.result


    def handle(self):
        if self.state == 'absent':
            self.handle_absent()
        elif self.state == 'present':
            self.handle_present()

        return

    
    def handle_absent(self):
        bucket = Bucket(name=self.name, id="0")
        for row in self.get_all():
            if row.name != self.name:
                continue
            bucket = row
            break
        
        if bucket.id == "0":
            return

        self.delete(bucket.id)
        self.result['changed'] = True
        self.result['msg'] = self.name + " has been deleted"

        return


    def handle_present(self):
        # Build empty bucket
        pre_bucket = Bucket(name=self.name, description=self.desc, id="0", retention_rules=BucketRetentionRules(type=self.retention['type'], every_seconds=int(self.retention['everySeconds'])))

        # fetch all buckets and save found bucket into pre_bucket
        for row in self.get_all().buckets:
            if row.name != self.name:
                continue
            pre_bucket = self.get_by_id(row.id)
            break

        # Create new bucket if not exists
        if pre_bucket.id == "0":
            bucket = self.create()
            if bucket.id == '0':
                self.result['changed'] = False
                self.result['msg'] = self.name + " cant create new bucket"

            self.result['changed'] = True
            self.result['msg'] = self.name + " has been created"
            return

        # TODO update bucket
        return

    def create(self) -> Bucket:
        orgApi = OrgApi(host=self.host, token=self.token)
        org = orgApi.get_by_name(self.org)
        if org.status != 'inactive':
            # TODO debug retention
            # test with molecule
            return self.client.create_bucket(bucket_name=self.name, bucket=Bucket(name=self.name, org_id=org.id, description=self.desc, retention_rules=BucketRetentionRules(type=self.retention['type'], every_seconds=int(self.retention['everySeconds']))))


        return Bucket(name='', id='0')


    def update(self, id) -> Bucket:
        return self.client.update_bucket(bucket=Bucket(name=self.name, description=self.desc, id=id, retention_rules=BucketRetentionRules(type=self.retention['type'], every_seconds=self.retention['everySeconds'])))

    
    def delete(self, id):
        return self.client.delete_bucket(bucket=id)


    def get_all(self) -> Buckets:
        return self.client.find_buckets()


    def get_by_id(self, id) -> Bucket:
        return self.client.find_buckets(name=self.name, org=self.org)