##
## You MUST update the following ## UPDATE HERE areas
##

import platform
from fabric.api import env, sudo, run, cd, prefix, require
from fabric.colors import green, red
from fabric.utils import abort

from os import environ, pardir
from os.path import abspath, basename, dirname, join, normpath, exists, isdir
from sys import path

from fabric.contrib import django


BASE_DIR = dirname(__file__)  #Project or Repo Base Dir
VIRTUALENV_DIR = dirname(dirname(__file__))

REPO_FOLDER_NAME = 'nswmicrosites_repo'
PROJECT_NAME = 'nswmicrosites'

## UPDATE HERE: Enter below the repository URL that will receive your new project code
PROJECT_REPO = 'git@djenie.git.beanstalkapp.com:/djenie/nswmicrosites.git'

## Here are the default NGINX and UPSTAR directories
NGINX_TARGET_FOLDER = '/etc/nginx'
GUNICORN_TARGET_FOLDER = '/etc/init'



def __get_env_pass__(environment):
    pass_env_var_name = '%s_%s' % (PROJECT_NAME.upper(), environment.upper())
    pass_env_var = environ.get(pass_env_var_name)
    if not pass_env_var:
        abort('You must set up the password using the SO variable: %s' % pass_env_var_name)
    return pass_env_var

def development():
    "Setup development (local) instance"
    env.environment = 'development'
    env.dev_mode = True
    env.hosts = ["localhost", ]
    env.server_url = 'localhost:8000'
    ## UPDATE HERE: Enter below your development workspace directory
    env.targetdir = '~/workspacepy/myprojects'


def staging():
    "Setup staging server"
    env.environment = 'staging'
    env.dev_mode = False
    env.server_url = 'simplesite.na-inter.net'
    env.hosts = [env.server_url, ]
    env.user = 'mechanics'
    env.password = __get_env_pass__('staging')
    env.targetdir = '/home/mechanics/envs'


def production():
    "Setup production server"
    env.environment = 'production'
    env.dev_mode = False
    ## UPDATE HERE: Enter below the staging server DOMAIN
    env.hosts = ["nswmicrosites.yourdomain.com", ]
    env.server_url = 'nswmicrosites.yourdomain.com'
    ## UPDATE HERE: Enter below a valid user that has SSH access to the above server
    env.user = 'user'
    env.password = __get_env_pass__('production')
    ## UPDATE HERE: Enter below the staging directory where the virtualenv will be created
    env.targetdir = '/home/user/envs'




def _create_virtualenv(targetdir, virtualenv_folder):
    print(green("**** Creating virtualenv"))
    with cd(targetdir):
        run("virtualenv %s" % virtualenv_folder)

def _clone_repository(targetdir, virtualenv_folder ):
    print(green("**** Cloning Repository"))
    with cd(targetdir):
        run("cd %s; git clone %s %s" % (virtualenv_folder, PROJECT_REPO, REPO_FOLDER_NAME))

def _install_project_dependencies(projectdir):
    print(green("**** Installing project dependencies"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('pip install -r ../requirements/%(environment)s.pip' % env)
            run('./manage.py bower_install --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _prepare_database(projectdir):
    print(green("**** Preparing Database"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py syncdb --noinput --no-initial-data --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))
            run('./manage.py migrate --all --no-initial-data --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))
            run('./manage.py migrate --all --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))


def _generate_nginx_entry(projectdir):
    print(green("**** Preparing NGINX entry"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py nginxentry --env %s --url %s --nginx %s --settings=%s.settings.%s' % (env.environment, env.server_url, NGINX_TARGET_FOLDER, PROJECT_NAME, env.environment))


def _generate_gunicorn_entry(projectdir, site_id='1'):
    print(green("**** Preparing GUNICORN entry: %s" % site_id))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py gunicornentry --env %s --user %s --site %s --settings=%s.settings.%s' % (env.environment, env.user, site_id, PROJECT_NAME, env.environment))

def _enable_nginx(projectdir):
    print(green("**** Enableing NGINX"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py nginxenable --env %s --nginx %s --settings=%s.settings.%s' % (env.environment, NGINX_TARGET_FOLDER, PROJECT_NAME, env.environment))

def _prepare_log_folder(targetdir, virtualenv_folder):
    print(green("**** Preparing Log folder"))
    with cd(targetdir):
        run('mkdir -p %s/logs' % virtualenv_folder)


def bootstrap():
    print(green("Bootstrap:: targetdir=%s" % env.targetdir))

    virtualenv_folder = "%s_%s" % (PROJECT_NAME, env.environment)
    repodir = join(env.targetdir, virtualenv_folder, REPO_FOLDER_NAME)
    projectdir = join(repodir, PROJECT_NAME)

    _create_virtualenv(env.targetdir, virtualenv_folder)
    _clone_repository(env.targetdir, virtualenv_folder)
    _install_project_dependencies(projectdir)
    _prepare_database(projectdir)
    if not env.dev_mode:
        _generate_nginx_entry(projectdir)
        _generate_gunicorn_entry(projectdir)
        _enable_nginx(projectdir)
        _prepare_log_folder(env.targetdir, virtualenv_folder)

    print(green("bootstrap DONE"))




def _update_code(projectdir):
    print(green("**** Updating repository"))
    with cd(projectdir):
        run("git pull")

def _migrate_database(projectdir):
    print(green("**** Migrating Database"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py migrate --all --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _update_assets(projectdir):
    print(green("**** Updating Assets (static files)"))
    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            run('./manage.py generate_colors --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))
            run('./manage.py collectstatic --noinput --settings=%s.settings.%s' % (PROJECT_NAME, env.environment))

def _reload_servers():
    print(green("**** Reloading servers (NGINX, GUNICORN"))
    GUNICORN_SERVICE = "gunicorn-%s_%s" % (PROJECT_NAME, env.environment)
    NGINX_SERVICE = "nginx"
    try:
        sudo("reload %s" % GUNICORN_SERVICE)
    except:
        sudo("start %s" % GUNICORN_SERVICE)
    sudo("service %s reload" % NGINX_SERVICE)


def deploy():
    print(green("Deploying :: %s (%s)" % (env.environment, env.hosts)))

    virtualenv_folder = "%s_%s" % (PROJECT_NAME, env.environment)
    repodir = join(env.targetdir, virtualenv_folder, REPO_FOLDER_NAME)
    projectdir = join(repodir, PROJECT_NAME)

    _update_code(projectdir)
    _install_project_dependencies(projectdir)
    _migrate_database(projectdir)
    if not env.dev_mode:
        _update_assets(projectdir)
        _reload_servers()
    
    print(green("Deploy DONE"))


def createsite(subdomain='new'):
    """ 
    Creates a new site entry 
    Usage: fab environment createsite:subdomain='newsite'
    """
    print(green("**** Creatig new site"))
    virtualenv_folder = "%s_%s" % (PROJECT_NAME, env.environment)
    repodir = join(env.targetdir, virtualenv_folder, REPO_FOLDER_NAME)
    projectdir = join(repodir, PROJECT_NAME)

    domain = '%s.webfoundry.com.au' % subdomain

    with cd(projectdir):
        with prefix('source ../../bin/activate'):
            site_id = run('./manage.py createsite --domain=%s --name=%s --settings=%s.settings.%s' % (domain, domain, PROJECT_NAME, env.environment))
            if not env.dev_mode:
                _generate_nginx_entry(projectdir)
                _generate_gunicorn_entry(projectdir, site_id)
                _enable_nginx(projectdir)
                _reload_servers()

