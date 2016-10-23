Deployment on Ubuntu Server
===========================

.. index:: How to create deployment files

You need to generate the NGINX / GUnicorn files by using the following commands

.. code-block:: bash

    ./manage.py nginxentry --url={{cookiecutter.domain_name}} --nginx=/etc/nginx --sitename={{cookiecutter.project_slug}} --env=staging

    ./manage.py nginxenable --url={{cookiecutter.domain_name}} --nginx=/etc/nginx --env=staging

    ./manage.py gunicornentry --user=myuser --url={{cookiecutter.domain_name}} --site=1 --env=staging
