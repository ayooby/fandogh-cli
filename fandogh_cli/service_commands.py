import click

from .fandogh_client import *
from .utils import login_required
from .config import get_project_config, get_user_config
from .presenter import present
from .base_commands import FandoghCommand


@click.group("service")
def service():
    pass


@click.command('logs', cls=FandoghCommand)
@click.option('--service_name', prompt='service_name', help="Service name")
@login_required
def service_logs(service_name):
    token_obj = get_user_config().get('token')
    logs = present(lambda: get_logs(service_name, token_obj))
    click.echo(logs)


@click.command("deploy", cls=FandoghCommand)
@click.option('--app', help='The image name', default=None)
@click.option('--version', '-v', prompt='The image version', help='The application version you want to deploy')
@click.option('--name', prompt='Your service name', help='Choose a unique name for your service')
@click.option('--env', '-e', 'envs', help='Environment variables (format: VARIABLE_NAME=VARIABLE_VALUE)', multiple=True)
@click.option('--port', '-p', 'port', help='The service port that will be exposed on port 80 to worldwide')
@login_required
def deploy(app, version, name, port, envs):
    token = get_user_config().get('token')
    if not app:
        app = get_project_config().get('app.name')
        if not app:
            click.echo('please declare the application name', err=True)

    pre = '''Your service deployed successfully.
The service is accessible via following link:
'''
    message = present(lambda: deploy_service(app, version, name, envs, port, token), pre=pre, field='url')
    click.echo(message)


@click.command('list', cls=FandoghCommand)
@click.option('-a', 'show_all', is_flag=True, default=False,
              help='show all the services regardless if it\'s running or not')
@login_required
def service_list(show_all):
    token = get_user_config().get('token')
    table = present(lambda: list_services(token, show_all),
                    renderer='table',
                    headers=['name', 'start date', 'state'],
                    columns=['name', 'start_date', 'state'])
    click.echo(table)


@click.command('destroy', cls=FandoghCommand)
@login_required
@click.option('--name', 'service_name', prompt='Name of the service you want to destroy', )
def service_destroy(service_name):
    token = get_user_config().get('token')
    message = present(lambda: destroy_service(service_name, token))
    click.echo(message)


service.add_command(deploy)
service.add_command(service_list)
service.add_command(service_destroy)
service.add_command(service_logs)
