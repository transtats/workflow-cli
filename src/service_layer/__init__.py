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

from src.service_layer.restclient import RestClient


def call_service(service_name):
    """
    decorator to call service
    :param service_name: API Config
    :return: response dict
    """
    def service_decorator(caller):
        def inner_decorator(url, resource, *args, **kwargs):
            rest_handle = RestClient(service_name)
            response = rest_handle.process_request(
                url, resource, *args, **kwargs
            )
            kwargs.update(dict(rest_response=response))
            return caller(url, resource, *args, **kwargs)
        return inner_decorator
    return service_decorator
