import click
import ast
from src.job_templates import get_job_template_by_type
from src.jobs_framework.runner.job_runner import JobRunnerWeblate, JobRunnerTransifex


def _fill_job_template_with_user_inputs(push_job_template, required_params: dict) -> dict:
    push_job_template_str = str(push_job_template.get_dict_form())
    for param in push_job_template.params:
        if param.lower() in required_params:
            respective_user_input = required_params[param.lower()]
            if not respective_user_input:
                print(f"Please provide value for {param}. See help.")
                exit(-1)
            push_job_template_str = \
                push_job_template_str.replace(param, required_params[param.lower()])
    return ast.literal_eval(push_job_template_str)


def _run_command(required_params: dict, push_job_template_with_inputs: dict):
    job_runner_map: dict = {
        'weblate': JobRunnerWeblate,
        'transifex': JobRunnerTransifex
    }
    job_runner = job_runner_map[required_params['repo_type']]()
    initialize_params: dict = {
        "required_params": required_params,
        "template_with_inputs": push_job_template_with_inputs
    }
    job_runner.bootstrap(initialize_params)
    job_runner.set_actions()
    job_runner.execute_tasks()


@click.command()
@click.option("--package-name", envvar='PACKAGE_NAME', help="Package Name")
@click.option("--project-uid", envvar='PROJECT_UID', help="Phrase Project UID")
@click.option("--target-langs", envvar='TARGET_LANGS', help="Target Languages")
@click.option("--repo-type", envvar='REPO_TYPE', help="Repository Type")
@click.option("--repo-branch", envvar='REPO_BRANCH', help="Repository Branch")
@click.option("--update", is_flag=False, help="Overwrite exiting Phrase Jobs")
@click.option("--prepend-branch", is_flag=False, help="Prepend branch to filename")
@click.pass_obj
def push(app_context, package_name, project_uid, target_langs, repo_type, update, repo_branch, prepend_branch):
    """Download translations from a Platform (Weblate, Transifex) and push to Phrase (Memsource)"""
    job_type: str = 'dpushtrans'
    required_params: dict = {
        'package_name': package_name,
        'project_uid': project_uid,
        'target_langs': target_langs,
        'repo_type': repo_type,
        'update': update,
        'repo_branch': repo_branch,
        'prepend_branch': prepend_branch
    }

    push_job_template = get_job_template_by_type(job_type)
    push_job_template_with_inputs: dict = \
        _fill_job_template_with_user_inputs(push_job_template, required_params)
    print("\nYour job is getting ready to be executed:")
    print(push_job_template_with_inputs)

    _run_command(required_params, push_job_template_with_inputs)
