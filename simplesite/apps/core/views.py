# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy


class ShowLandingPageView(TemplateView):
    template_name = "core/landingpage.html"

    def get_context_data(self, **kwargs):
        context = super(ShowLandingPageView, self).get_context_data(**kwargs)
        context['site_title'] = 'Simple Site'
        return context
