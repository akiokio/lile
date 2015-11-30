import os
from contextlib import contextmanager
from tempfile import mkdtemp

from fabric.api import cd, env, local, prefix, run, settings, sudo, task
from fabric.operations import put

STAGING_HOST = '52.35.8.141'
SSHKEY_PATH = '~/.ssh/lile_prod.pem'

@contextmanager
def _virtualenv():
    with prefix(env.activate):
        yield


def _manage_py(command):
    run('python manage.py %s' % command)

@task
def deploy():
    with cd(env.root_dir):
        run('git pull origin %s' % env.branch)
        with _virtualenv():
            run('pip install -r requirements.txt')
    with cd(env.code_dir):
        with _virtualenv():
            run('python manage.py collectstatic --noinput')
            if env.should_compress:
                run('python manage.py compress')
            # run('python manage.py syncdb --noinput')
            run('python manage.py migrate')

    restart()

@task
def restart():
    """
    Reload nginx/gunicorn
    """
    with settings(warn_only=True):
        sudo('supervisorctl restart %s' % env.supervisor_id)
        sudo('/etc/init.d/nginx reload')


@task
def staging():
    env.remote = 'staging'
    env.branch = 'master'
    env.key_filename = SSHKEY_PATH
    env.host = STAGING_HOST
    env.username = 'ubuntu'
    env.port = 22
    env.host_string = '%s@%s' % (env.username, env.host)
    env.root_dir = '/srv/www/lile'
    env.code_dir = '%s/lile' % env.root_dir
    env.venvs = '/srv/www'
    env.virtualenv = '%s/env' % env.venvs
    env.activate = 'source %s/bin/activate ' % env.virtualenv
    env.should_compress = False
    env.supervisor_id = "lile"
