# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import ListHomes,PagesView

urlpatterns = [
    path('', ListHomes.as_view(), name='home'),

    # Coincide con cualquier archivo HTML
    re_path(r'^.*\.*', PagesView.as_view(), name='pages'),
]
