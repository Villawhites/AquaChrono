from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from djchoices import ChoiceItem, DjangoChoices
from django.core.validators import MinValueValidator, MaxValueValidator

from core.custom_fields import RutField
# Create your models here.
class Representative(models.Model):
    """
    Apoderado alumnos
    """
    id = models.AutoField(primary_key=True)
    # current_representative = models.ForeignKey(
    #     'student.Student',
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Alumno")
    # )
    name = models.CharField(max_length=50, verbose_name=_("Nombres"))
    last_name = models.CharField(max_length=50, verbose_name=_("Apellidos"))
    rut = RutField(verbose_name=_("Rut"), unique=True,null=True,blank=False)
    email = models.EmailField(null=True,blank=False, max_length=30)
    phone = models.BigIntegerField(
        null=True,
        validators=[MinValueValidator(10_000_000),
                                        MaxValueValidator(99_999_999_999_999),],
        verbose_name=_("Teléfono")
    )
    password_representative = models.CharField(
        max_length=50,
        verbose_name=_("Contraseña")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Apoderado")
        verbose_name_plural = _("Apoderados")

