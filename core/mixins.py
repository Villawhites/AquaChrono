
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View



# class BaseCurrentCompany(LoginRequiredMixin):

#     def dispatch(self, request, *args, **kwargs):

#         if request.user.is_authenticated:
#             company_id = self.request.session.get('current_company', None)
#             current_year = self.request.session.get('current_year', None)

#             try:
#                 company = Company.objects.get(id=company_id)
#             except Company.DoesNotExist:
#                 return render(request, 'app/company_not_selected.html')

#             if not current_year:
#                 return render(request, 'app/company_not_selected.html')

#         return super().dispatch(request, *args, **kwargs)


class ProtectDeleteMixin(LoginRequiredMixin):
    """
        Protege en caso de que el objeto se desea eliminar pero tiene
         relaciones con otros objetos.
    """
    def dispatch(self, request, *args, **kwargs):
        is_related = False
        obj = self.get_object()
        if request.user.is_authenticated:
            for rel in obj._meta.get_fields():
                try:
                    related = rel.related_model.objects.filter(**{rel.field.name: obj})
                    if related.exists():
                        is_related = True
                except AttributeError:
                    pass
        if is_related:
            # Como hay relación
            messages.error(request, f'{obj._meta.verbose_name} está en uso.')
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)


class TabFunctionMixin():
    """
    Se necesita añadir una variable en la clase llamada:
    variable_session_tab para que el mixin funcione y trabaje sobre esa variable
    de sesión.
    """
    variable_session_tab = None

    def update_session_tab(self, number_tab=None):
        last_url = self.request.META.get('HTTP_REFERER', None)
        actual_url = self.request.path
        if last_url and actual_url:
            actual_url = self._clean_actual_url(actual_url)
            if actual_url and actual_url not in last_url:
                number_tab = 1
        actual_value = self.request.\
            session.get(self.variable_session_tab, 1)
        self.request.session\
            [self.variable_session_tab]=\
                number_tab if number_tab else actual_value

    def _clean_actual_url(self, actual_url_str):
        """
        Método diseñado para funcionar solo cuando el menú principal de una
        vista que usa tabs tiene el patron de url de la siguiente forma:
        /url_texto/url_text/123/url_text/url_texto
        el regex buscará el / y despues un valor numérico y despues el /, para
        encontrar el /123/ y de ahí buscará el texto anterior a eso para
        obtener la base de la url principal donde está el tab y así encontrar
        esa base en la url principal del tab.
        """
        out_url_text_first_uuid_or_id = re.search(
            '/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}/',
            actual_url_str
            )
        if not out_url_text_first_uuid_or_id:
            out_url_text_first_uuid_or_id = re.search('/[0-9]+/', actual_url_str)
            if not out_url_text_first_uuid_or_id:
                return None

        return actual_url_str[0:out_url_text_first_uuid_or_id.end()]


# class ContractMixin():
#     """
#     Debe llegar por la url el uuid del contrato o el id y mixin extraerá la información
#     necesaria de ese contrato, contra el mes y el año.

#     variables a enviar por url:
#     - <str: uuid_contract>
#     - <int: id_contract>
#     """
#     contract = None

#     def dispatch(self, request, *args, **kwargs):
#         id_contract = kwargs.get('id_contract', None)
#         uuid_contract = kwargs.get('uuid_contract', None)

#         if id_contract or uuid_contract:
#             current_month = request.session.get('current_month', None)
#             current_year = request.session.get('current_year', None)
#             current_company = request.session.get('current_company', None)
#             kwargs_filter = {
#                 'company':current_company,
#                 'year':current_year,
#                 'month':current_month,
#             }
#             if id_contract:
#                 kwargs_filter['id']= id_contract
#             elif uuid_contract:
#                 kwargs_filter['uuid']= uuid_contract

#             self.contract = get_object_or_404(Contract, **kwargs_filter)

#             # Creación de calculationsall en caso de que no exista. Este código
#             # es debido a un bug de la api de creación de contrato, y es que
#             # en algunos casos no crea la instancia de calculationsall del contract.
#             # Entonces aquí se fuerza la creación del objeto calculationsAll.
#             try:
#                 self.contract.calculationsall
#             except CalculationsAll.DoesNotExist:
#                 monthly_parameters = MonthlyParameters.objects.filter(
#                     month=current_month,
#                     year=current_year
#                 ).first().id
#                 monthly_parameters_company = MonthlyParametersCompany.objects.get(
#                     month=current_month,
#                     year=current_year,
#                     company=current_company
#                 ).id
#                 CalculationsAll.objects.create(
#                     contract_id=self.contract.id,
#                     monthly_parameters_id=monthly_parameters,
#                     monthly_parameters_company_id=monthly_parameters_company)

#         return super().dispatch(request, *args, **kwargs)

#     def get_employee(self):
#         if not self.contract:
#             return None
#         return self.contract.employee

#     def get_workinformationemployee(self):
#         if not self.contract:
#             return None
#         return self.contract.workinformationemployee

#     def get_previtionalinformationemployee(self):
#         if not self.contract:
#             return None
#         return self.contract.previtionalinformationemployee

#     def get_familyburdenvalue(self):
#         if not self.contract:
#             return None
#         return self.contract.familyburdenvalue

#     def get_monthlymovement(self):
#         if not self.contract:
#             return None
#         return self.contract.monthlymovement

#     def get_calculationsall(self):
#         if not self.contract:
#             return None
#         return self.contract.calculationsall