# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import StudentCreate,StudentList,StudentLists,StudentEdit,StudentDelete


urlpatterns = [
    path('create/',StudentCreate.as_view(),name="create_student"),
    path('list/',StudentLists.as_view(),name="list_students"),
    path('list_student/',StudentList.as_view(),name="list_student"),
    path('edit/<int:pk>/', StudentEdit.as_view(), name='edit_student'),
    path('delete/<int:pk>/', StudentDelete.as_view(), name="delete_student"),
]
