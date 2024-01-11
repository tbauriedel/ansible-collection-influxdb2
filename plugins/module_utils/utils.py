"""InfluxDB v2 API utilites"""
#!/usr/bin/python3

import json
import requests

class Influx2Api:
    '''
    Common api requests to for InfluxDBv2
    '''

    api_token: str
    endpoint: str
    timeout: int

    def __init__(self, token, host) -> None:
        '''
        Initialize API class
        '''
        self.api_token, self.endpoint, self.timeout = token, host, 10


    # Organizations

    def get_all_orgs(self) -> json:
        '''
        Get all organizations from InfluxDB. Queries.
        Returns JSON.
        '''

        headers = {
            'Authorization': 'Token ' + self.api_token
        }
        response = requests.get(self.endpoint + '/api/v2/orgs', headers=headers, timeout=self.timeout)

        return json.loads(response.content)


    def get_orgid_by_name(self, name) -> str:
        '''
        Get organization ID by name. Returns ID
        If no organization is found by name, 'not found' will be returned.
        '''

        orgs = self.get_all_orgs()

        for org in orgs['orgs']:
            if org['name'] == name:
                return org['id']

        return "not found"


    # Buckets

    def get_bucketid_by_name(self, name, org): # pyling
        '''
        Get bucket ID by name. Returns ID
        If no bucket is found by name, 'not found' will be returned
        '''

        headers = {
            'Authorization': 'Token ' + self.api_token
        }

        url = self.endpoint + '/api/v2/buckets?name=' + name + "&orgID=" + self.get_orgid_by_name(org)
        response = requests.get(url, headers=headers, timeout=self.timeout)
        json_resp = json.loads(response.content)

        for bucket in json_resp['buckets']:
            return bucket['id']

        return "not found"


    def get_bucket_status(self, name, org_id):
        '''
        Get state of single bucket of org from InfluxDB. Returns 'present' if found and 'absent' if not present.
        '''

        headers = {
            'Authorization': 'Token ' + self.api_token
        }

        url = self.endpoint + '/api/v2/buckets?name=' + name + "&orgID=" + org_id
        response = requests.get(url, headers=headers, timeout=self.timeout)
        json_resp = json.loads(response.content)

        if "code" in json_resp:
            if json_resp["code"] == "not found":
                return "absent"

        for bucket in json_resp["buckets"]:
            if bucket['name'] == name:
                return 'present'

            return 'absent'


    def create_bucket(self, name, org_id, retention):
        '''
        Create bucket
        '''

        headers = {
            'Authorization': 'Token ' + self.api_token,
            'Content-type': 'application/json'
        }

        url = self.endpoint + '/api/v2/buckets'
        payload = {
            'orgID': org_id,
            'name': name,
            'retentionRules': [
                {
                    'type': retention['type'],
                    'everySeconds': int(retention['everySeconds']),
                    'shardGroupDurationSeconds': int(retention['shardGroupDurationSeconds'])
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=self.timeout)

        return response.status_code, response.content


    def delete_bucket(self, name, org):
        '''
        Delete bucket
        '''

        headers = {
            'Authorization': 'Token ' + self.api_token
        }

        url = self.endpoint + '/api/v2/buckets/' + self.get_bucketid_by_name(name, org)
        response = requests.delete(url, headers=headers, timeout=self.timeout)

        return response.status_code, response.content
