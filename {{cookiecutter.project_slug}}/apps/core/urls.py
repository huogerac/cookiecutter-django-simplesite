# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from .views import ShowLandingPageView

urlpatterns = patterns('',  # noqa

    url(r'^$', ShowLandingPageView.as_view(),
       name='core.landingpage'),

)
