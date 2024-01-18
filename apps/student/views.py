from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
#from django_filters.views import View
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Student
from .tables import StudentTable
from core.filters import GenericFilter


# Create your views here.
# class ListHome(View):
#     model = Student
#     template_name = 'home/index.html'

#     def get(self, request, *args, **kwargs):
#         context = {'segment': 'index'}
#         context['data_student'] = Student.objects.all()

#         html_template = loader.get_template('home/index.html')
#         return HttpResponse(html_template.render(context, request))