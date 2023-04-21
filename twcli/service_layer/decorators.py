# Copyright 2020 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import requests
from twcli.config import get_config, get_config_item
from twcli.constants import TRANSPLATFORM_ENGINES, API_TOKEN_PREFIX, GIT_PLATFORMS
from twcli.service_layer.config.memsource import \
    resources as memsource_resources, media_types as memsource_media_types

GITHUB_TOKEN = get_config_item(get_config(), "github", "token")


def request_phrase_token(phrase_user: str, phrase_pass: str):
    config = memsource_resources.get('request_token')
    payload, headers = {}, {}
    payload.update(dict(userName=phrase_user))
    payload.update(dict(password=phrase_pass))
    headers['Accept'] = memsource_media_types[0]
    headers['Content-Type'] = memsource_media_types[0]

    phrase_api_url = get_config_item(get_config(), "target", "url")
    auth_api_url = phrase_api_url + "/api2/v1" + config.mount_point
    response = requests.post(url=auth_api_url, json=payload, headers=headers)
    if not response.ok:
        print("Please ensure Phrase credentials are correct in the config.")
        exit(-1)
    response_json = response.json()
    return response_json.get("token", "")


def set_api_auth():
    """
    decorator to set authentication for API calls
    :return:
    """
    def service_decorator(caller):
        def inner_decorator(rest_client, url, resource, *args, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            if rest_client.service == TRANSPLATFORM_ENGINES[4]:
                # Memsource needs token in Authorization header.
                memsource_auth_user = API_TOKEN_PREFIX.get(rest_client.service) or kwargs['auth_user']
                latest_token = request_phrase_token(kwargs['auth_user'], kwargs['auth_token'])
                kwargs['headers']['Authorization'] = f"{memsource_auth_user} {latest_token}"
            if kwargs.get('auth_user') and kwargs.get('auth_token'):
                auth_tuple = ()
                if rest_client.service == TRANSPLATFORM_ENGINES[1]:
                    # Transifex need auth_tuple for HTTPBasicAuth.
                    auth_tuple = (
                        API_TOKEN_PREFIX.get(rest_client.service) or kwargs['auth_user'],
                        kwargs['auth_token']
                    )
                elif rest_client.service == TRANSPLATFORM_ENGINES[2]:
                    # Zanata needs credentials in the header.
                    kwargs['headers']['X-Auth-User'] = kwargs['auth_user']
                    kwargs['headers']['X-Auth-Token'] = kwargs['auth_token']
                elif rest_client.service == TRANSPLATFORM_ENGINES[3]:
                    # Weblate needs credentials in the headers either.
                    weblate_auth_user = API_TOKEN_PREFIX.get(rest_client.service) or kwargs['auth_user']
                    kwargs['headers']['Authorization'] = f"{weblate_auth_user} {kwargs['auth_token']}"
                kwargs.update(dict(auth_tuple=auth_tuple))
            if rest_client.service == GIT_PLATFORMS[0] and GITHUB_TOKEN:
                # Setting up auth header for GitHub
                kwargs['headers']['Authorization'] = f"Bearer {GITHUB_TOKEN}"
            return caller(rest_client, url, resource, *args, **kwargs)
        return inner_decorator
    return service_decorator
