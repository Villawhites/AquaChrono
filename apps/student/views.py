from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django_filters.views import FilterView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin

from .models import Student
from .tables import StudentTable
from core.filters import GenericFilter


# Create your views here.
def ListHome(request):
    context = {'segment': 'index'}
    context['data_student'] = Student.objects.all()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
# class ListHome(LoginRequiredMixin, View):
#     model = Student
#     template_name = 'templates/home/index.html'  # Asegúrate de que esta ruta sea correcta

#     def get(self, request):
#         context = {}
#         qs = Student.objects.all()
#         context['data_student'] = qs
#         return render(request, self.template_name, context)