Deployment on Ubuntu Server
===========================

.. index:: How to create deployment files

You need to generate the NGINX / GUnicorn files by using the following commands

.. code-block:: bash

    ./manage.py nginxentry --url={{domain_name}} --nginx=/etc/nginx --sitename=project_slug --env=staging

    ./manage.py nginxenable --url={{domain_name}} --nginx=/etc/nginx --env=staging

    ./manage.py gunicornentry --user=mechanics --url={{domain_name}} --site=1 --env=staging
