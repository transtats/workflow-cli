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
import os
from abc import ABC

from src.config import get_config, get_config_item
from src.jobs_framework.ds import TaskList
from src.jobs_framework.action_mapper import ActionMapper
from src.jobs_framework import BASE_DIR


class JobRunner(ABC):
    action_mapper = None

    def __init__(self) -> None:
        self.tasks_ds: TaskList = TaskList()
        self.config = get_config()
        self.job_base_dir: str = \
            os.path.join(BASE_DIR, "jobs_framework", "runner", "sandbox")

    def bootstrap(self, initialize_params: dict) -> None:
        raise NotImplementedError()

    def __create_action_mapper(self) -> None:
        self.action_mapper = ActionMapper(
            self.tasks_ds,
            self.job_base_dir,
            getattr(self, 'tag', ''),
            getattr(self, 'package', ''),
            getattr(self, 'hub_url', ''),
            getattr(self, 'buildsys', ''),
            getattr(self, 'release', ''),
            getattr(self, 'repo_branch', ''),
            getattr(self, 'ci_pipeline_uuid', ''),
            getattr(self, 'upstream_repo_url', ''),
            getattr(self, 'upstream_l10n_url', ''),
            getattr(self, 'trans_file_ext', ''),
            getattr(self, 'pkg_upstream_name', ''),
            getattr(self, 'pkg_downstream_name', ''),
            getattr(self, 'pkg_branch_map', {}),
            getattr(self, 'pkg_tp_engine', ''),
            getattr(self, 'pkg_tp_auth_usr', ''),
            getattr(self, 'pkg_tp_auth_token', ''),
            getattr(self, 'pkg_tp_url', ''),
            getattr(self, 'pkg_ci_engine', ''),
            getattr(self, 'pkg_ci_url', ''),
            getattr(self, 'pkg_ci_auth_usr', ''),
            getattr(self, 'pkg_ci_auth_token', ''),
            getattr(self, 'ci_release', ''),
            getattr(self, 'ci_target_langs', []),
            getattr(self, 'ci_project_uid', ''),
            getattr(self, 'ci_lang_job_map', {}),
            getattr(self, 'log_file', ''),
        )

    def set_actions(self) -> None:
        self.__create_action_mapper()
        self.action_mapper.set_actions()

    def execute_tasks(self) -> None:
        try:
            self.action_mapper.execute_tasks()
        except Exception as e:
            setattr(self, 'exception', e)
            raise Exception(e)


class JobRunnerWeblate(JobRunner):
    """
    Job Runner with Weblate Configurations
    """
    def bootstrap(self, initialize_params: dict) -> None:
        print("\nBootstrapping the Job Runner")
        print(f"\n {self.job_base_dir}")
        api_token = get_config_item(self.config, "server", "token")
        print(f"Token coming from config {api_token}")
        print(initialize_params)


class JobRunnerTransifex(JobRunner):
    """
    Job Runner with Transifex Configurations
    """

    def bootstrap(self, initialize_params: dict) -> None:
        initialize_params = initialize_params
        print("\nBootstrapping the Job Runner")
        print(f"\n {self.job_base_dir}")
        print(initialize_params)
