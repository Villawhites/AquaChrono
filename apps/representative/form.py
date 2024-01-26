from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Column, Div, Field,
                                Hidden, Layout, MultiField,
                                Row, Submit, Fieldset)
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import Representative


class CreateRepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative

        fields = [
            'rut',
            'name',
            'last_name',
            'email',
            'phone',
            'password_representative'
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
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'data-parsley-email-validation': '',
                    'data-parsley-error-message': _(
                        'Por favor ingrese un correo electrónico válido.'),
                    'maxlength': '30'
                }
            ),
            # 'phone': forms.TextInput(
            #     attrs={
            #         'class': 'form-control',
            #         'onkeypress': 'return onlyNumberKey(event)',
            #         'maxlength': "9",
            #         "placeholder": "942353523",
            #     }
            # ),
            'password_representative':forms.TextInput(
                attrs={
                    'class': 'form-control pass-en-gris',
                    'type': 'password',
                    'required': 'required',
                    'maxlength': '50',
                    "placeholder": "Contraseña",
                }
            ),
        }
    email_2 = forms.CharField(
        label=_("Correo"),
        widget=forms.TextInput(
            attrs={
                'data-parsley-email-validation': '',
                'data-parsley-error-message': _(
                    'Por favor ingrese un correo electrónico válido.'),
                'maxlength': '30',
                'class': 'campo-en-gris'

            }
        ),
    )
    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^9\d{8}$',  # Asegura que comience con "9" y tenga en total 9 dígitos
                message='Ingrese un número de teléfono válido que comience con "9" y tenga 9 dígitos',
            ),
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'maxlength': "9",
                "placeholder": "942353523",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)
        super(CreateRepresentativeForm, self).__init__(*args, **kwargs)
        self.fields['rut'].help_text = 'Rut con guion y sin puntos.'
        submit_text = "Actualizar" if self.instance.pk else "Guardar"
        self.fields['email'].label = 'Correo'
        self.fields['email_2'].widget.attrs['disabled'] = True
        self.fields['email_2'].required = False
        self.fields['phone'].label = 'Celular'

        self.helper = FormHelper()
        url_cancel = reverse('representative:list_representatives')
        self.helper.form_class = 'form-parsley'
        self.helper.include_media = True
        self.helper.layout = Layout(
            Div(
                Column(
                Fieldset(
                        'Datos Personales',
                        Row(
                            Column('rut', css_class='col-md-3'),
                            Column('name', css_class='col-md-4'),
                            Column('last_name', css_class='col-md-4'),
                            Hidden('representative_form', '1'),#bank_movement
                            css_class="justify-content-md-left"
                            ),#ROW1
                        ),#Fieldset1
                Fieldset(
                        'Datos Contacto',
                        Row(
                            Column('email', css_class='col-md-4 '),
                            Column('phone', css_class='col-md-4'),
                            css_class="justify-content-md-left"),
                        ),#Fieldset2
                Fieldset(
                        'Datos Cuenta',
                        Row(
                            Column('email_2', css_class='col-md-4'),
                            Column('password_representative', css_class='col-md-4'),
                            css_class="justify-content-md-left"),
                        ),#Fieldset3
                    css_class="col-md-12"),#COLUMN 1
                ),#DIV
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
        name = self.cleaned_data.get('name')
        last_name = self.cleaned_data.get('last_name')

        if not all(char.isalpha() or char.isspace() for char in name):
           self.add_error('name','El nombre solo debe contener letras.')

        if not all(char.isalpha() or char.isspace() for char in last_name):
           self.add_error('last_name','El Apellido solo debe contener letras.')


class ConfirmDeleteForm(forms.ModelForm):
    """
    Confirmacion eliminacion Apoderado
    """
    class Meta:
        model = Representative
        fields = []

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        url_costcenter = reverse('representative:list_representatives')

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