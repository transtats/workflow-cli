import os
from dataclasses import dataclass, field
from typing import List

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


@dataclass
class JobTemplate:
    name: str
    type: str
    tasks: List[str] = field(default_factory=list)

    def __str__(self):
        tasks: str = ", ".join(self.tasks)
        return f"Job template '{self.name}' is of type '{self.type}' and has '{tasks}' tasks."


def parse_job_template(job_template_file_path: str) -> JobTemplate:
    job_name: str = ""
    job_type: str = ""
    job_tasks: List[str] = []
    try:
        with open(job_template_file_path, 'r') as yaml_file_stream:
            parsed_job_template: dict = yaml.safe_load(yaml_file_stream)
            job_name = parsed_job_template['job']['name']
            job_type = parsed_job_template['job']['type']
            for tasks in parsed_job_template['job']['tasks']:
                job_tasks.extend(list(tasks.keys()))
    except yaml.YAMLError as exc:
        print(exc)
    except IndexError as exc:
        print(exc)
    return JobTemplate(job_name, job_type, job_tasks)


def get_job_templates() -> List[JobTemplate]:
    job_templates_path: str = os.path.join(BASE_DIR, "data", "job_templates")
    job_templates: List[JobTemplate] = []
    for _, _, files in os.walk(job_templates_path):
        for file in files:
            yaml_job_template_file_path: str = os.path.join(job_templates_path, file)
            parsed_job_template: JobTemplate = parse_job_template(yaml_job_template_file_path)
            job_templates.append(parsed_job_template)
    return job_templates
