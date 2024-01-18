# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import ListHome

urlpatterns = [
    path('', ListHome, name='index'),
    # Otros patrones de URL si los tienes
]