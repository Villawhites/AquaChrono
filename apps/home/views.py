# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django.views import View
from django.shortcuts import render
from django.template.loader import get_template

from apps.student.models import Student

class ListHomes(View):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        qs = Student.objects.all()
        context = {'data_student': qs}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class PagesView(View):
    template_404 = 'home/page-404.html'
    template_500 = 'home/page-500.html'

    def get_template_name(self, request):
        load_template = request.path.split('/')[-1]
        return 'home/' + load_template

    def get(self, request, *args, **kwargs):
        context = {}
        try:
            if request.path.split('/')[-1] == 'admin':
                return HttpResponseRedirect(reverse('admin:index'))

            context['segment'] = self.get_template_name(request)
            html_template = loader.get_template(self.get_template_name(request))
            return HttpResponse(html_template.render(context, request))

        except template.TemplateDoesNotExist:
            html_template = loader.get_template(self.template_404)
            return HttpResponse(html_template.render(context, request))

        except Exception:
            html_template = loader.get_template(self.template_500)
            return HttpResponse(html_template.render(context, request))


