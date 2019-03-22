#!/usr/bin/env python

"""
    Simple class to interact with BitBaan MALab's API.
    https://malab.bitbaan.com
"""

import urllib.request
import requests
import json

USER_AGENT = "BitBaan-API-Sample-Python"


class MALabLib:
    server_address = ''
    api_key = ''

    def __init__(self, server_address, api_key=''):
        self.server_address = server_address
        self.api_key = api_key

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

    @staticmethod
    def handle_return_value(return_value):
        if return_value is False:
            return {'success': False, 'error_code': 900}
        else:
            return return_value

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
