#!/usr/bin/env python

"""
    Simple class to interact with BitBaan MALab's API.
    https://malab.bitbaan.com
"""

import urllib.request
import urllib.error
import requests
import json
import hashlib

USER_AGENT = "BitBaan-API-Sample-Python"


class MALabLib:
    server_address = ''
    api_key = ''

    def __init__(self, server_address, api_key=''):
        self.server_address = server_address
        self.api_key = api_key

    @staticmethod
    def handle_return_value(return_value):
        if return_value is False:
            return {'success': False, 'error_code': 900}
        else:
            return return_value

    @staticmethod
    def get_sha256(file_path):
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    """
    Returns:
        If the function fails, the return value is False.
    """
    def call_api_with_json_input(self, api, json_input):
        try:
            req = urllib.request.Request(self.server_address + "/" + api)
            req.add_header("Content-type", "application/json")
            req.add_header("User-Agent", USER_AGENT)
            json_data_as_bytes = json.dumps(json_input).encode('utf-8')
            req.add_header('Content-Length', len(json_data_as_bytes))
            response = urllib.request.urlopen(req, json_data_as_bytes)
            data = response.read()
            values = json.loads(data)
            return values
        except urllib.error.HTTPError as e:
            data = e.read()
            values = json.loads(data)
            return values
        except Exception:
            return False

    def call_api_with_form_input(self, api, data_input, file_param_name, file_path):
        try:
            files = {file_param_name, open(file_path, 'rb')},
            response = requests.post(self.server_address + "/" + api,
                                     files=files,
                                     data=data_input)
            values = response.json()
            return values
        except Exception:
            return False

    """
    Returns:
        If the function succeeds, the return value is 0.
        If the function fails, the return value is error code.
    """
    def login(self, email, password):
        params = {'email': email, 'password': password}
        returned_value = self.call_api_with_json_input('api/v1/user/login', params)
        returned_value = self.handle_return_value(returned_value)
        if returned_value["success"] is True:
            self.api_key = returned_value['apikey']
        return returned_value

    def scan(self, file_path, file_name, is_private=False, file_origin=''):
        params = {'filename': file_name, 'apikey': self.api_key}
        if is_private is True:
            params["is_private"] = True
        if len(file_origin) != 0:
            params["fileorigin"] = file_origin
        returned_value = self.call_api_with_form_input('api/v1/scan', params, 'filedata', file_path)
        return self.handle_return_value(returned_value)

    def rescan(self, file_sha256):
        params = {'sha256': file_sha256, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/rescan', params)
        return self.handle_return_value(returned_value)

    def results(self, file_sha256, scan_id):
        params = {'sha256': file_sha256, 'scan_id': scan_id, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/search/scan/results', params)
        return self.handle_return_value(returned_value)

    def search_by_hash(self, sha256, ot=None, ob=None, page=None, per_page=None):
        params = {'hash': sha256, 'apikey': self.api_key}
        if ot is not None:
            params["ot"] = ot
        if ob is not None:
            params["ob"] = ob
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        returned_value = self.call_api_with_json_input('api/v1/search/scan/hash', params)
        return self.handle_return_value(returned_value)

    def search_by_malware_name(self, malware_name, ot=None, ob=None, page=None, per_page=None):
        params = {'malware_name': malware_name, 'apikey': self.api_key}
        if ot is not None:
            params["ot"] = ot
        if ob is not None:
            params["ob"] = ob
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        returned_value = self.call_api_with_json_input('api/v1/search/scan/malware-name', params)
        return self.handle_return_value(returned_value)

    def download_file(self, hash_value):
        params = {'hash': hash_value, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/file/download', params)
        return self.handle_return_value(returned_value)

    def get_comments(self, sha256, page=None, per_page=None):
        params = {'sha256': sha256, 'apikey': self.api_key}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        returned_value = self.call_api_with_json_input('api/v1/comment', params)
        return self.handle_return_value(returned_value)

    def add_comment(self, sha256, description):
        params = {'sha256': sha256, 'description': description, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/comment/add', params)
        return self.handle_return_value(returned_value)

    def edit_comment(self, comment_id, new_description):
        params = {'comment_id': comment_id, 'description': new_description, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/comment/edit', params)
        return self.handle_return_value(returned_value)

    def delete_comment(self, comment_id):
        params = {'comment_id': comment_id, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/comment/delete', params)
        return self.handle_return_value(returned_value)

    def approve_comment(self, comment_id):
        params = {'comment_id': comment_id, 'apikey': self.api_key}
        returned_value = self.call_api_with_json_input('api/v1/comment/approve', params)
        return self.handle_return_value(returned_value)

    def get_captcha(self):
        params = {}
        returned_value = self.call_api_with_json_input('api/v1/captcha', params)
        return self.handle_return_value(returned_value)

    def register(self, first_name, last_name, username, email, password, captcha):
        params = {'firstname': first_name,
                  'lastname': last_name,
                  'username': username,
                  'email': email,
                  'password': password,
                  'captcha': captcha}
        returned_value = self.call_api_with_json_input('api/v1/user/register', params)
        return self.handle_return_value(returned_value)
