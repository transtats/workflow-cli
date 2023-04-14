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
import shutil
from abc import abstractmethod

from src.config import get_config, get_config_item
from src.jobs_framework.ds import TaskList
from src.jobs_framework.parser import YMLJobParser
from src.jobs_framework.action_mapper import ActionMapper
from src.jobs_framework import BASE_DIR


class JobRunner:
    action_mapper = None

    def __init__(self) -> None:
        self.tasks_ds: TaskList = TaskList()
        self.config = get_config()
        self.job_base_dir: str = \
            os.path.join(BASE_DIR, "runner", "sandbox")
        self.log_file = os.path.join(self.job_base_dir, "job-runner.log")

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

    def inform_user(self):
        print(os.linesep)
        print("Bootstrap is done. Executing Job ..")
        print(f"See logs here: file://{self.log_file}")
        print(os.linesep)

    def conclude_user(self):
        print(os.linesep)
        print("Job Execution is now Complete!")
        print(os.linesep)

    @abstractmethod
    def bootstrap(self, initialize_params: dict) -> None:
        raise NotImplementedError()


class JobRunnerPush(JobRunner):
    """
    Job Runner for Push Jobs
    """

    def _set_data_from_config(self):
        pkg_name = get_config_item(self.config, "package", "name")
        if pkg_name != self.package:
            print(f"Input package differs from config. Please check!")
            exit(-1)
        self.upstream_repo_url = get_config_item(self.config, "package", "upstream_repo_url")
        self.upstream_l10n_url = get_config_item(self.config, "package", "upstream_l10n_url")
        self.trans_file_ext = get_config_item(self.config, "package", "trans_file_ext")
        self.pkg_upstream_name = get_config_item(self.config, "package", "upstream_name")
        self.pkg_downstream_name = get_config_item(self.config, "package", "downstream_name")

        self.pkg_tp_engine = get_config_item(self.config, "source", "engine")
        self.pkg_tp_auth_usr = get_config_item(self.config, "source", "auth_usr")
        self.pkg_tp_auth_token = get_config_item(self.config, "source", "auth_token")
        self.pkg_tp_url = get_config_item(self.config, "source", "url")

        self.pkg_ci_engine = get_config_item(self.config, "target", "engine")
        self.pkg_ci_url = get_config_item(self.config, "target", "url")
        self.pkg_ci_auth_usr = get_config_item(self.config, "target", "auth_usr")
        self.pkg_ci_auth_token = get_config_item(self.config, "target", "auth_pass")

    def _set_data_from_yml_job(self, yml_job: YMLJobParser):
        self.yml_job_name = yml_job.job_name
        self.job_type = yml_job.job_type
        self.package = yml_job.package
        self.release = yml_job.release
        self.buildsys = yml_job.buildsys
        self.tag = ""
        if isinstance(yml_job.tags, list) and len(yml_job.tags) > 0:
            self.tag = yml_job.tags[0]
        elif isinstance(yml_job.tags, str):
            self.tag = yml_job.tags

    def _set_job_params(self, param_value_pair: dict):
        for param, value in param_value_pair.items():
            setattr(self, param, value)
            if param == "project_uid":
                setattr(self, "ci_project_uid", value)
            if param == "target_langs":
                if isinstance(value, (list, tuple)):
                    setattr(self, "ci_target_langs", value)
                elif isinstance(value, str) and "," in value:
                    setattr(self, "ci_target_langs", value.split(","))
                    setattr(self, param, value.split(","))

    def _set_tasks(self, yml_job: YMLJobParser):
        tasks = yml_job.tasks
        for task in tasks:
            self.tasks_ds.add_task(task)

    def _set_log_file(self):
        if self.package and self.job_type:
            self.log_file = os.path.join(
                self.job_base_dir, f"job-{self.package}-{self.job_type}.log"
            )

    def _wipe_workspace(self):
        """This makes sandbox clean for a new job to run"""
        # remove log file if exists
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        for file in os.listdir(self.job_base_dir):
            file_path = os.path.join(self.job_base_dir, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path) and not file_path.endswith('.py'):
                os.unlink(file_path)

    def bootstrap(self, initialize_params: dict) -> None:
        self._wipe_workspace()
        yml_job = YMLJobParser(initialize_params['template_with_inputs'])
        self._set_data_from_yml_job(yml_job)
        self._set_data_from_config()
        self._set_job_params(initialize_params['required_params'])
        self._set_tasks(yml_job)
        self._set_log_file()


class JobRunnerPull(JobRunner):
    """
    Job Runner for Pull Jobs
    """

    def _set_data_from_config(self):
        pkg_name = get_config_item(self.config, "package", "name")
        if pkg_name != self.package:
            print(f"Input package differs from config. Please check!")
            exit(-1)
        self.upstream_repo_url = get_config_item(self.config, "package", "upstream_repo_url")
        self.upstream_l10n_url = get_config_item(self.config, "package", "upstream_l10n_url")
        self.trans_file_ext = get_config_item(self.config, "package", "trans_file_ext")
        self.pkg_upstream_name = get_config_item(self.config, "package", "upstream_name")
        self.pkg_downstream_name = get_config_item(self.config, "package", "downstream_name")

        self.pkg_tp_engine = get_config_item(self.config, "source", "engine")
        self.pkg_tp_auth_usr = get_config_item(self.config, "source", "auth_usr")
        self.pkg_tp_auth_token = get_config_item(self.config, "source", "auth_token")
        self.pkg_tp_url = get_config_item(self.config, "source", "url")

        self.pkg_ci_engine = get_config_item(self.config, "target", "engine")
        self.pkg_ci_url = get_config_item(self.config, "target", "url")
        self.pkg_ci_auth_usr = get_config_item(self.config, "target", "auth_usr")
        self.pkg_ci_auth_token = get_config_item(self.config, "target", "auth_pass")

    def _set_data_from_yml_job(self, yml_job: YMLJobParser):
        self.yml_job_name = yml_job.job_name
        self.job_type = yml_job.job_type
        self.package = yml_job.package
        self.release = yml_job.release
        self.buildsys = yml_job.buildsys
        self.tag = ""
        if isinstance(yml_job.tags, list) and len(yml_job.tags) > 0:
            self.tag = yml_job.tags[0]
        elif isinstance(yml_job.tags, str):
            self.tag = yml_job.tags

    def _set_job_params(self, param_value_pair: dict):
        for param, value in param_value_pair.items():
            setattr(self, param, value)
            if param == "project_uid":
                setattr(self, "ci_project_uid", value)
            if param == "target_langs":
                if isinstance(value, (list, tuple)):
                    setattr(self, "ci_target_langs", value)
                elif isinstance(value, str) and "," in value:
                    setattr(self, "ci_target_langs", value.split(","))
                    setattr(self, param, value.split(","))

    def _set_tasks(self, yml_job: YMLJobParser):
        tasks = yml_job.tasks
        for task in tasks:
            self.tasks_ds.add_task(task)

    def _set_log_file(self):
        if self.package and self.job_type:
            self.log_file = os.path.join(
                self.job_base_dir, f"job-{self.package}-{self.job_type}.log"
            )

    def _wipe_workspace(self):
        """This makes sandbox clean for a new job to run"""
        # remove log file if exists
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        for file in os.listdir(self.job_base_dir):
            file_path = os.path.join(self.job_base_dir, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path) and not file_path.endswith('.py') \
                    and not file_path.endswith('.log'):
                os.unlink(file_path)

    def bootstrap(self, initialize_params: dict) -> None:
        self._wipe_workspace()
        yml_job = YMLJobParser(initialize_params['template_with_inputs'])
        self._set_data_from_yml_job(yml_job)
        self._set_data_from_config()
        self._set_job_params(initialize_params['required_params'])
        self._set_tasks(yml_job)
        self._set_log_file()
