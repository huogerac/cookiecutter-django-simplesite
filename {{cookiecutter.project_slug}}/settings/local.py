# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import os
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
#TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


# Mail settings
# ------------------------------------------------------------------------------
#EMAIL_PORT = 1025
#EMAIL_HOST = 'localhost'

# CACHING
# ------------------------------------------------------------------------------
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': ''
#    }
#}

# django-debug-toolbar
# ------------------------------------------------------------------------------
#MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#INSTALLED_APPS += ('debug_toolbar', )
#INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )
