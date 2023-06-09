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

import json
import click

from typing import Callable

from twcli.version import version
from twcli.job_templates import templates
from twcli.push_translations import push
from twcli.pull_translations import pull
from twcli.config import get_config, get_config_item

APP_VERSION = "0.1.0"


class AppContext(object):
    """
    CLI Application Context Data
    """
    def __init__(self):
        self.version = APP_VERSION
        self.config = get_config()

    @staticmethod
    def print_r(result_dict):
        click.echo(json.dumps(result_dict, indent=4, sort_keys=True))


CLICommand = Callable[[AppContext], click.Command]


@click.group()
@click.pass_context
def entry_point(ctx):
    """
    Transtats Localization Workflow CLI
    """
    ctx.obj = AppContext()


entry_point.add_command(version)
entry_point.add_command(templates)
entry_point.add_command(push)
entry_point.add_command(pull)
