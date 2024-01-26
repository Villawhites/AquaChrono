# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),            # UI Kits Html files
    path('student/', include(("apps.student.urls",'student'), namespace='student')),
    path('representative/', include(("apps.representative.urls",'representative'), namespace='representative')),
    path('trainer/', include(("apps.trainer.urls",'trainer'), namespace='trainer')),
    path('competition/', include(("apps.competition.urls",'competition'), namespace='competition')),
]
