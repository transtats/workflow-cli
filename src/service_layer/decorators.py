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

# dashboard
from src.constants import TRANSPLATFORM_ENGINES, API_TOKEN_PREFIX, GIT_PLATFORMS


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
