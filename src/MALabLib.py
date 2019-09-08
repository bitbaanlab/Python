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
    def get_sha256(file_path):
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    @staticmethod
    def get_error(return_value):
        error = ''
        if "error_code" in return_value:
            error += ("Error code: %d\n" % return_value["error_code"])
        if "error_desc" in return_value:
            error += ("Error description: %s\n" % return_value["error_desc"])
        if "error_details_code" in return_value:
            error += ("Error details code: %d\n" % return_value["error_details_code"])
        if "error_details_desc" in return_value:
            error += ("Error details description: %s\n" % return_value["error_details_desc"])
        if "status_code" in return_value:
            error += ("Status code: %d\n" % return_value["status_code"])
            if return_value["status_code"] == 422 and "error" in return_value:
                for key in return_value["error"]:
                    error += ("Validation in: %s, %s\n" % (key, return_value["error"][key]))
        return error

    def call_with_json_input(self, api, json_input):
        try:
            req = urllib.request.Request(self.server_address + "/malab/v1/" + api)
            req.add_header("Content-type", "application/json")
            req.add_header("User-Agent", USER_AGENT)
            json_data_as_bytes = json.dumps(json_input).encode('utf-8')
            req.add_header('Content-Length', len(json_data_as_bytes))
            response = urllib.request.urlopen(req, json_data_as_bytes)
            data = response.read()
            values = json.loads(data)
            return values
        except urllib.error.HTTPError as e:
            try:
                data = e.read()
                values = json.loads(data)
                return values
            except:
                return {"success": False, "error_code": 900}
        except:
            return {"success": False, "error_code": 900}

    def call_with_form_input(self, api, data_input, file_param_name, file_path):
        try:
            with open(file_path, 'rb') as file_handle:
                files = [(file_param_name, ("file_to_upload", file_handle, "application/octet-stream"))]
                response = requests.post(self.server_address + "/malab/v1/" + api,
                                         files=files,
                                         data=data_input)
                values = response.json()
                return values
        except:
            return {"success": False, "error_code": 900}
