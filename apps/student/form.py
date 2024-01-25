from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Column, Div, Field, Hidden, Layout, Row,
                                 Submit)
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _
from datetime import datetime, date
from django.core.exceptions import ValidationError

from .models import Student


class CreateStundentForm(forms.ModelForm):
    #class Media:
        # js = (
        #     'js/student/student.js'
        # )
        # # css = {
        # #     'all': ('parsley/parsley.css',)
        # # }

    class Meta:
        model = Student

        fields = [
            'rut',
            'name',
            'birth_date'
        ]

        widgets = {
            'rut': forms.TextInput(
                attrs={
                    'type': 'text',
                    'data-parsley-chilean-rut': '',
                    'data-parsley-trigger': 'input',
                    'required': 'required',
                    'maxlength': "12"
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'required': 'required',
                }
            ),
           'birth_date': forms.DateInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'date',  # Añadido el atributo type
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreateStundentForm, self).__init__(*args, **kwargs)
        self.fields['rut'].help_text = 'Rut con guion y sin puntos.'
        submit_text = "Actualizar" if self.instance.pk else "Guardar"
        self.helper = FormHelper()
        url_cancel = reverse('student:list_students')
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = True
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('rut', css_class='col-md-2'),
                    Column('name', css_class='col-md-5'),
                    Column('birth_date',css_class='col-md-4'),
                    Hidden('student_form', '1'),#bank_movement
                    css_class="justify-content-md-center"
                ),
            ),
            Row(
                HTML(
                    '<a class="btn btn-lg btn-warning mr-0 ml-2 my-1"'
                    ' href="' + url_cancel + '">'+_('Cancelar')+'</a>'
                ),
                Submit(
                        'submit', _(f'{submit_text}'),
                    css_class='btn btn-primary btn-lg float-right mr-0 ml-2 my-1'),
                css_class="d-flex justify-content-end pt-3 mr-0"
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date', None)
        year_birth= birth_date.year
        month_birth= birth_date.month
        day_birth= birth_date.day
        comparative_date=datetime(datetime.now().year,datetime.now().month,15).date()
        str_birth_date=datetime(birth_date.year,birth_date.month,birth_date.day).date()
        name = self.cleaned_data.get('name')

        if not all(char.isalpha() or char.isspace() for char in name):
           self.add_error('name','El nombre solo debe contener letras.')

        #***DESCOMENTAR PARA PRUEBAS, COMENTAR PARA PODER USAR FECHA HOY
        # if comparative_date:
        #     if str_birth_date > comparative_date:
        #         self.add_error('birth_date', "La Fecha Nacimiento No puede ser superior al mes y año de proceso")

class ConfirmDeleteForm(forms.ModelForm):
    """
    Confirmacion eliminacion Alumno
    """
    class Meta:
        model = Student
        fields = []

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        url_costcenter = reverse('student:list_students')

        self.helper = FormHelper()
        self.helper.form_class = 'form-parsley'
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML(
                        '<a class="btn btn-lg btn-warning"'
                        ' href="' + url_costcenter + '">'+_('Cancelar')+'</a>'
                    ),
                    Submit(
                            'submit','Confirmar',
                        css_class='btn btn-primary btn-lg float-right'),
                    css_class="d-flex justify-content-end"
                )
            ),
        )