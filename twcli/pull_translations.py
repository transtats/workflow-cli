import click
import ast
from twcli.job_templates import get_job_template_by_type
from twcli.jobs_framework.runner.job_runner import JobRunnerPull


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
    job_runner = JobRunnerPull()
    initialize_params: dict = {
        "required_params": required_params,
        "template_with_inputs": push_job_template_with_inputs
    }
    job_runner.bootstrap(initialize_params)
    job_runner.set_actions()
    job_runner.inform_user()
    job_runner.execute_tasks()
    job_runner.conclude_user()


@click.command()
@click.option("--package-name", envvar='PACKAGE_NAME', help="Package Name")
@click.option("--project-uid", envvar='PROJECT_UID', help="Phrase Project UID")
@click.option("--target-langs", envvar='TARGET_LANGS', help="Target Languages")
@click.option("--workflow-step", envvar='WORKFLOW_STEP', help="Workflow Step")
@click.option("--repo-type", envvar='REPO_TYPE', help="Repository Type")
@click.option("--repo-branch", envvar='REPO_BRANCH', help="Repository Branch")
@click.pass_obj
def pull(app_context, package_name, project_uid, target_langs, workflow_step, repo_type, repo_branch):
    """Download translations from Phrase (Memsource) and submit back to a Platform (Weblate, Transifex)"""
    job_type: str = 'pulltrans'
    required_params = {
        'package_name': package_name,
        'project_uid': project_uid,
        'target_langs': target_langs,
        'workflow_step': workflow_step,
        'repo_type': repo_type,
        'repo_branch': repo_branch
    }

    pull_job_template = get_job_template_by_type(job_type)
    pull_job_template_with_inputs = \
        _fill_job_template_with_user_inputs(pull_job_template, required_params)
    _run_command(required_params, pull_job_template_with_inputs)
