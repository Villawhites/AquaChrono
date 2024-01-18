# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from djchoices import ChoiceItem, DjangoChoices

from core.custom_fields import RutField

# Create your models here.
# class Student(models.Model):
#     """
#     Alumno Natacion
#     """
#     class competitions(DjangoChoices):
#         BRAZO1 = ChoiceItem(1, _("Brazo1"))
#         BRAZO2 = ChoiceItem(2, _("Brazo2"))
#         BRAZO3 = ChoiceItem(3, _("Brazo3"))
#         BRAZO4 = ChoiceItem(4, _("Brazo4"))
#         BRAZO5 = ChoiceItem(5, _("Brazo5"))

#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, verbose_name=_("Nombre Alumno"))
#     rut = RutField(verbose_name=_("Rut"), unique=True,null=True,blank=False)
#     birth_date = models.DateField(
#         verbose_name=_("Fecha de Nacimiento"),
#         null=True,
#         blank=True)
#     time = models.CharField(max_length=50, verbose_name=_("Tiempo"),null=True,)
#     competitiontypes = models.SmallIntegerField(verbose_name="Competencia",
#         choices=competitions,null=True,)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _("Alumno")
#         verbose_name_plural = _("Alumnos")

# class CompetitionType(models.Model):
#     """
#     Tipo Competencia
#     """
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, verbose_name=_("Nombre Competencia"))

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _("Competencia")
#         verbose_name_plural = _("Competencias")
