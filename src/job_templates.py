import click
import os
from dataclasses import dataclass, field
from typing import List

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


@dataclass
class JobTemplate:
    name: str
    type: str
    _dict: dict = field(default_factory=dict)
    tasks: List[str] = field(default_factory=list)
    params: List[str] = field(default_factory=list)

    def __str__(self):
        tasks: str = ", ".join(self.tasks)
        params: str = ", ".join(self.params)
        return f"Job template '{self.name}' is of type '{self.type}' and has '{tasks}' " \
               f"tasks with '{params}' params."

    def get_dict_form(self):
        return self._dict


def find_job_params(parsed_job_template: dict) -> List[str]:
    cap_values = []
    for _, value in parsed_job_template.items():
        if isinstance(value, str) and value.isupper():
            cap_values.append(value)
        elif isinstance(value, dict):
            results = find_job_params(value)
            for result in results:
                cap_values.append(result)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = find_job_params(item)
                    for another_result in more_results:
                        cap_values.append(another_result)
    return list(set(cap_values))


def parse_job_template(job_template_file_path: str) -> JobTemplate:
    job_name: str = ""
    job_type: str = ""
    _dict: dict = {}
    job_tasks: List[str] = []
    job_params: List[str] = []
    try:
        with open(job_template_file_path, 'r') as yaml_file_stream:
            parsed_job_template: dict = yaml.safe_load(yaml_file_stream)
            job_name = parsed_job_template['job']['name']
            job_type = parsed_job_template['job']['type']
            for tasks in parsed_job_template['job']['tasks']:
                job_tasks.extend(list(tasks.keys()))
            job_params = find_job_params(parsed_job_template)
            _dict = parsed_job_template
    except yaml.YAMLError as exc:
        print(exc)
    except IndexError as exc:
        print(exc)
    return JobTemplate(job_name, job_type, _dict, job_tasks, job_params)


def get_job_templates() -> List[JobTemplate]:
    job_templates_path: str = os.path.join(BASE_DIR, "data", "job_templates")
    job_templates: List[JobTemplate] = []
    for _, _, files in os.walk(job_templates_path):
        for file in files:
            yaml_job_template_file_path: str = os.path.join(job_templates_path, file)
            parsed_job_template: JobTemplate = parse_job_template(yaml_job_template_file_path)
            job_templates.append(parsed_job_template)
    return job_templates


def get_job_template_by_type(job_type: str) -> JobTemplate or None:
    push_job_templates = list(filter(lambda template: template.type == job_type, get_job_templates()))
    if not push_job_templates:
        return
    return push_job_templates[0]


@click.command()
def templates():
    """List available job templates."""
    available_job_templates: List[JobTemplate] = get_job_templates()
    for idx, template in enumerate(available_job_templates):
        print(f"{idx+1}. {template}")
