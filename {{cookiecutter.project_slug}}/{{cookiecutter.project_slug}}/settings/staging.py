# -*- coding: utf-8 -*-
"""
Staging settings

"""

import os
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ['*',]  # TODO: Add the specific env url
