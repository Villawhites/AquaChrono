from datetime import timedelta
import re

from django.core.validators import EMPTY_VALUES
from django.db import models
from django.forms import ValidationError
from django.forms.fields import RegexField, CharField
from django.utils.translation import gettext_lazy as _

# from itertools import cycle


class CLRutField(RegexField):
    """
    Chilean "Rol Unico Tributario" (RUT) field. This is the Chilean national
    identification number.
    Samples for testing are available from
    https://palena.sii.cl/cvc/dte/ee_empresas_emisoras.html
    """
    default_error_messages = {
        'invalid': _('Ingrese un rut valido.'),
        'strict': _('Enter a valid Chilean RUT. The format is XX.XXX.XXX-X.'),
        'checksum': _('El RUT igresado no es valido.'),
    }

    def __init__(self, *args, **kwargs):

        if 'strict' in kwargs:
            del kwargs['strict']
            super().__init__(
                r'^(\d{1,2}\.)?\d{3}\.\d{3}-[\dkK]$',
                error_message=self.default_error_messages['strict'],
                *args, **kwargs
            )
        else:
            # In non-strict mode, accept RUTs that validate but do not exist in
            # the real world.
            super().__init__(r'^[\d\.]{1,11}-?[\dkK]$', *args, **kwargs)

    def clean(self, value):
        """
        Check and clean the Chilean RUT.
        """
        super().clean(value)
        if value in EMPTY_VALUES:
            return u''
        rut, verificador = self._canonify(value)
        if self._algorithm(rut) == verificador:
            return self._format(rut, verificador)
        else:
            raise ValidationError(self.error_messages['checksum'])

    def _algorithm(self, rut):
        """
        Takes RUT in pure canonical form, calculates the verifier digit.
        """
        suma = 0
        multi = 2

        for r in rut[::-1]:
            suma += int(r) * multi
            multi += 1
            if multi == 8:
                multi = 2

        return '0123456789K0'[11 - suma % 11]

    def _canonify(self, rut):
        """
        Turns the RUT into one normalized format. Returns a (rut, verifier)
        tuple.
        """
        rut = re.sub('[^0-9kK]', '', rut)

        return rut[:-1], rut[-1].upper()

    def _format(self, code, verifier=None):
        """
        Formats the RUT from canonical form to the common string representation.
        If verifier=None, then the last digit in 'code' is the verifier.
        """
        if verifier is None:
            verifier = code[-1]
            code = code[:-1]
        while len(code) > 3 and '.' not in code[:3]:
            pos = code.find('.')
            if pos == -1:
                new_dot = -3
            else:
                new_dot = pos - 3
            code = code[:new_dot] + '.' + code[new_dot:]

        return '{}-{}'.format(code, verifier)


class RutField(models.Field):

    description = "Rut field for save cleand and validate"

    default_error_messages = {
        'invalid_rut': _("El rut ingresado no es valido."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def value_to_string(self, obj):
        value = self.value_from_object(obj)

        return self.get_prep_value(value)

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None

        value = re.sub('[^0-9kK]', '', value)

        return value

    def to_python(self, value):
        if value:
            if value.find('-') < 0:
                return "{}.{}.{}-{}".format(
                    value[:-7], value[-7:-4], value[-4:-1], value[-1]
                )
            else:
                return value
        return ""

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)

    def formfield(self, **kwargs):
        # The widget is allready being specified
        # somewhere by models.DateField...

        defaults = {
            'form_class': CLRutField
        }
        defaults.update(kwargs)

        return super().formfield(**defaults)


class DurationTimeField(models.Field):
    """
    MODELS
    1.Importar libreria
        from app.custom_fields import DurationTimeField
    2. Crear un field de modelo
        duration = DurationTimeField(
            null=True,
            blank=True,
            verbose_name=_("Duración")
        )

    MODELFORMS
    0. Importar
        from app.functions import timedelta_to_str
    1. En los widgets
            'duration': forms.TextInput(
                    attrs={
                        'type': 'text',
                        'data-parsley-duration-validation': '',
                'onkeypress': 'return onlyDurationKey(event)',
                        'data-parsley-trigger': 'input',
                        'maxlength': "5"
                    }
                ),
    2. En el init
        if self.instance.pk:
            self.initial['duration'] =\
                        timedelta_to_str(self.instance.duration)

    """
    description = "DurationField as hh:mm format"

    default_error_messages = {
        'invalid_rut': _("Formato incorrecto (hh:mm)."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'DurationField'

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        value = self._string_format(value)

        # return self.get_prep_value(value)
        return value

    def get_db_prep_value(self, value, *args, **kwargs):

        if value in EMPTY_VALUES:
            return None

        return value

    def to_python(self, value):
        if value:
            # self._string_format(value)
             return value
        return ""

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)
        # return value

    def _string_format(self, value):
        minutes = value.days * 1440
        seconds = value.seconds / 60
        total_minutes = minutes + seconds
        hours = int(total_minutes // 60)
        real_minutes = int(total_minutes % 60)

        return '{}:{}'.format(hours, real_minutes)

    def formfield(self, **kwargs):
        # The widget is allready being specified
        # somewhere by models.DateField...

        defaults = {
            'form_class': DurationField
        }
        defaults.update(kwargs)

        return super().formfield(**defaults)

class DurationField(CharField):
    """
    """
    default_error_messages = {
        'strict': _('Ingrese un formato válido. (HH:MM)'),
    }

    def __init__(self, *args, **kwargs):
        widget = kwargs.get('widget', None)
        if widget:
            widget.attrs.update({'placeholder':'00:00'})
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """
        Check and clean the HH:MM format
        """
        # super().clean(value)
        if value in EMPTY_VALUES:
            return None

        if len(value) > 5:
            raise ValidationError(self.default_error_messages['strict'])

        if not re.search('^([0-9]?[0-9]):([0-5]?[0-9])$', value):
            raise ValidationError(self.default_error_messages['strict'])

        hours, minutes = self._canonify(value)
        if not hours.isdigit():
            raise ValidationError(self.default_error_messages['strict'])
        if not minutes.isdigit():
            raise ValidationError(self.default_error_messages['strict'])

        return self._format(hours, minutes)

    def _canonify(self, value):
        """
        Turns the duration in normalized format. Returns a (hours, minutes)
        tuple.
        """
        list_values = value.split(':')
        return list_values[0], list_values[1]

    def _format(self, hours, minutes):
        """
        Formats
        """
        return timedelta(
                hours=int(hours),
                minutes=int(minutes),
            )
