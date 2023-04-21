# Copyright 2023 Red Hat, Inc.
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

"""
Configuration file related functions
"""
from __future__ import absolute_import
import os
import click
from six.moves import configparser


def get_config():
    """
    Get the information about config file path
    :return: ConfigParser object
    """
    config = configparser.ConfigParser()
    home_dir = os.path.expanduser('~')
    paths = [
        os.path.join(home_dir, '.config', 'transtats.conf'),
    ]
    if os.environ.get('TRANSTATS_TEST_CONFIG', 'false').lower() == 'true':
        test_config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../tests/test_transtats.conf'))
        paths.append(test_config_path)

    # Check for any custom config file path availablility
    custom_config_path = os.environ.get('TRANSTATS_CONFIG_PATH')
    if custom_config_path:
        if os.path.exists(custom_config_path):
            paths.append(custom_config_path)

    if not any(os.path.exists(path) for path in paths):
        raise click.ClickException('No configuration file was found')

    config.read(paths)
    return config


def get_config_item(config, section, item):
    """
    Get the value of a config item and
    throws a ClickException if it doesn't exist
    """
    try:
        return config.get(section, item)
    except (configparser.NoOptionError, configparser.NoSectionError, configparser.InterpolationSyntaxError):
        error_msg = ('The item "{0}" is not set correctly in the "{1}" section '
                     'in your config file.'.format(item, section))
        raise click.ClickException(error_msg)
