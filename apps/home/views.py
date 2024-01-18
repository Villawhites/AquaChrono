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

from apps.student.models import Student

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['data_student'] = Student.objects.all()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Table list Alumnos
# class StudentView(LoginRequiredMixin,SingleTableMixin,FilterView):

#     model = Student
#     table_class = StudentTable
#     template_name = 'home/index.html'
#     # filterset_class= GenericFilter
#     # filter_fields = ['contract__employee__code', 'contract__employee__rut', 'contract__employee__name','contract__employee__last_name']
#     # variable_session_tab = 'template_tab_severance_pay'
#     # table_pagination = {
#     #     "per_page": 20
#     # }
#     # fields_search = [
#     #     'contract__employee__code',
#     #     'contract__employee__rut',
#     #     'contract__employee__name',
#     #     'contract__employee__last_name'
#     #     ]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

#     def get_queryset(self):
#         self.filterset_class.filter_fields = self.table_class.Meta.fields

#         queryset = self.model.objects.all()


#         return queryset