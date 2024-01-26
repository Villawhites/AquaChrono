# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import RepresentativeCreate,RepresentativeList,RepresentativeLists,RepresentativeEdit,RepresentativeDelete

urlpatterns = [
    path('create/',RepresentativeCreate.as_view(),name="create_representative"),
    path('list/',RepresentativeLists.as_view(),name="list_representatives"),
    path('list_representative/',RepresentativeList.as_view(),name="list_representative"),
    path('edit/<int:pk>/', RepresentativeEdit.as_view(), name='edit_representative'),
    path('delete/<int:pk>/', RepresentativeDelete.as_view(), name="delete_representative"),
]
