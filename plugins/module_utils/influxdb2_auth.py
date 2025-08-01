# !/usr/bin/python3

# Copyright (c) 2025, Tobias Bauriedel <tobias@bauriedel.de>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

from influxdb_client import Permission, PermissionResource, Authorization
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.api import Api
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_organization import OrgApi
from ansible_collections.tbauriedel.influxdb2.plugins.module_utils.influxdb2_bucket import BucketApi


class AuthApi():
    SUPPORTED_RESOURCES = {
        "buckets": {
            "resolver": "bucket",
            "type": "buckets"
        },
        "dashboards": {
            "resolver": None,
            "type": "dashboards"
        },
        "tasks": {
            "resolver": None,
            "type": "tasks"
        },
        "orgs": {
            "resolver": None,
            "type": "orgs"
        },
        "users": {
            "resolver": None,
            "type": "users"
        },
        "authorizations": {
            "resolver": None,
            "type": "authorizations"
        },
        "secrets": {
            "resolver": None,
            "type": "secrets"
        },
        "variables": {
            "resolver": None,
            "type": "variables"
        },
        "labels": {
            "resolver": None,
            "type": "labels"
        },
        "telegrafs": {
            "resolver": None,
            "type": "telegrafs"
        },
        "checks": {
            "resolver": None,
            "type": "checks"
        },
        "notificationsRules": {
            "resolver": None,
            "type": "notificationRules"
        },
        "notificationEndpoints": {
            "resolver": None,
            "type": "notificationEndpoints"
        },
        "scrapers": {
            "resolver": None,
            "type": "scrapers"
        },
        "remotes": {
            "resolver": None,
            "type": "remotes"
        },
        "replications": {
            "resolver": None,
            "type": "replications"
        },
        "flows": {
            "resolver": None,
            "type": "flows"
        }
    }

    def __init__(self, host, token, name, org, state, desc=None, permissions=None, verify_ssl=True, result=None):
        self.name = name
        self.host = host
        self.token = token
        self.org = org
        self.state = state
        self.desc = desc
        self.permissions = permissions or []
        self.verify_ssl = verify_ssl
        self.result = result or {"changed": False}

        self.client = Api.new_client(host=host, token=token, verify_ssl=verify_ssl).authorizations_api()
        self.org_api = OrgApi(host=host, token=token, verify_ssl=verify_ssl)
        self.bucket_api = BucketApi(name="", state="", desc="", host=host, token=token, org=org, retention={}, verify_ssl=verify_ssl, result={})

    def return_result(self):
        return self.result

    def handle(self):
        if self.state == 'absent':
            self.handle_absent()
        elif self.state == 'present':
            self.handle_present()
        return

    def handle_absent(self):
        org = self.org_api.get_by_name(self.org)
        if not org:
            self.result['changed'] = False
            self.result['msg'] = f"Org '{self.org}' not found."
            return

        # Naive match: look for description == name
        for auth in self.client.find_authorizations(org_id=org.id):
            if auth.description == self.name:
                self.client.delete_authorization(auth.id)
                self.result['changed'] = True
                self.result['msg'] = f"Token '{self.name}' deleted"
                return

        self.result['changed'] = False
        self.result['msg'] = f"No token named '{self.name}' found"
        return

    def handle_present(self):
        org = self.org_api.get_by_name(self.org)
        if not org or org.status != 'active':
            self.result['failed'] = True
            self.result['msg'] = f"Organization '{self.org}' not found or inactive"
            return

        influx_permissions = self._build_permissions(org_id=org.id)

        existing_token = None
        for token in self.client.find_authorizations(org_id=org.id):
            if token.description == self.name:
                existing_token = token
                break

        if existing_token:
            if self._compare_permissions(existing_token.permissions, influx_permissions):
                self.result['changed'] = False
                self.result['msg'] = f"Token '{self.name}' already exists with same permissions"
                self.result['token'] = existing_token.token
                return
            else:
                self.client.delete_authorization(existing_token.id)
                self.result['changed'] = True
                self.result['msg'] = f"Token '{self.name}' permissions changed -> recreated"
        else:
            self.result['changed'] = True
            self.result['msg'] = f"Token '{self.name}' created"

        # Create token
        auth_obj = Authorization(
            org_id=org.id,
            permissions=influx_permissions,
            description=self.name
        )
        auth = self.client.create_authorization(authorization=auth_obj)
        self.result['token'] = auth.token
        return

    def _compare_permissions(self, existing_perms, desired_perms):
        """Compares two sets of permissions for actual equality."""
        def serialize(perm):
            return {
                "action": perm.action,
                "type": perm.resource.type,
                "id": str(perm.resource.id),
                "org_id": str(perm.resource.org_id)
            }
        
        print("foo")

        existing_set = sorted([serialize(p) for p in existing_perms], key=lambda x: (x["action"], x["type"], x["id"]))
        desired_set = sorted([serialize(p) for p in desired_perms], key=lambda x: (x["action"], x["type"], x["id"]))

        return existing_set == desired_set

    def _build_permissions(self, org_id):
        influx_permissions = []

        for perm_block in self.permissions:
            for resource_type, actions in perm_block.items():
                if resource_type not in self.SUPPORTED_RESOURCES:
                    raise Exception(f"Unsupported permission type: {resource_type}")

                config = self.SUPPORTED_RESOURCES[resource_type]

                for action_entry in actions:
                    action = action_entry['action']
                    resource_id = None

                    # ggf. ID lookup für Ressourcen, die eine benannte Entität benötigen
                    if config["resolver"] == "bucket":
                        bucket_name = action_entry["bucket"]
                        bucket = self.bucket_api.get_by_name(bucket_name)
                        if not bucket:
                            raise Exception(f"Bucket '{bucket_name}' not found")
                        resource_id = bucket.id

                    resource = PermissionResource(
                        type=config["type"],
                        id=resource_id,
                        org_id=org_id
                    )
                    influx_permissions.append(Permission(action=action, resource=resource))

        return influx_permissions