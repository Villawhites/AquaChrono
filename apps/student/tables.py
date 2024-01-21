from django.urls import reverse
import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2 import A, LinkColumn
from django.utils.html import format_html

from .models import Student



class StudentTable(tables.Table):
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'rut',
        ]

