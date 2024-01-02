#!/usr/bin/python3

import json
import requests

class InfluxApi():
    '''
    Common api requests to for InfluxDBv2
    '''
    def get_bucket_status(module):
        '''
        Get state of single bucket of org from InfluxDB. Returns 'present' if found and 'absent' if not present.
        '''
        headers = {
            'Authorization': 'Token ' + module.params['token']
        }

        url = module.params['host'] + '/api/v2/buckets?name=' + module.params['name'] + "&orgID=" + InfluxApi.get_orgID_by_name(module)
        response = requests.get(url, headers=headers)
        json_resp = json.loads(response.content)

        if "code" in json_resp:
            if json_resp["code"] == "not found":
                return "absent"

        for bucket in json_resp["buckets"]:
            if bucket['name'] == module.params['name']:
                return 'present'
            else:
                return 'absent'


    def get_all_orgs(module):
        '''
        Get all organizations from InfluxDB. Queries.
        Returns JSON.
        '''

        headers = {
            'Authorization': 'Token ' + module.params['token']
        }
        response = requests.get(module.params['host'] + '/api/v2/orgs', headers=headers)

        return json.loads(response.content)


    def get_orgID_by_name(module):
        '''
        Get organization ID by name. Returns ID
        If no organization is found by name, 'not found' will be returned.
        '''

        orgs = InfluxApi.get_all_orgs(module)

        for org in orgs['orgs']:
            if org['name'] == module.params['org']:
                return org['id']
        
        return "not found"


    def create_bucket(module):
        '''
        Create bucket
        '''

        headers = {
            'Authorization': 'Token ' + module.params['token'],
            'Content-type': 'application/json'
        }

        url = module.params['host'] + '/api/v2/buckets'
        payload = {
            'orgID': InfluxApi.get_orgID_by_name(module),
            'name': module.params['name'],
            'retentionRules': [
                {
                    'type': module.params['retention']['type'],
                    'everySeconds': int(module.params['retention']['everySeconds']),
                    'shardGroupDurationSeconds': int(module.params['retention']['shardGroupDurationSeconds'])
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        return response.status_code, response.content


    def get_bucketID_by_name(module):
        '''
        Get bucket ID by name. Returns ID
        If no bucket is found by name, 'not found' will be returned
        '''

        headers = {
            'Authorization': 'Token ' + module.params['token']
        }

        url = module.params['host'] + '/api/v2/buckets?name=' + module.params['name'] + "&orgID=" + InfluxApi.get_orgID_by_name(module)
        response = requests.get(url, headers=headers)
        json_resp = json.loads(response.content)

        for bucket in json_resp['buckets']:
            return bucket['id']

        return "not found"


    def delete_bucket(module):
        '''
        Delete bucket
        '''

        headers = {
            'Authorization': 'Token ' + module.params['token']
        }

        url = module.params['host'] + '/api/v2/buckets/' + InfluxApi.get_bucketID_by_name(module)
        response = requests.delete(url, headers=headers)

        return response.status_code, response.content