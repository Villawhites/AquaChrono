from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse,reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import DeleteView
from django.db.models import ProtectedError

from .models import Representative
from .form import CreateRepresentativeForm,ConfirmDeleteForm

# Create your views here.
class RepresentativeCreate(CreateView):
    model = Representative
    form_class = CreateRepresentativeForm
    template_name = 'representative/representative_create.html'
    success_url = reverse_lazy('representative:create_representative')

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(RepresentativeCreate, self)\
    #         .get_form_kwargs(*args, **kwargs)
    #     ids_representantes = Representative.objects.values_list('id', flat=True)
    #     for ids in ids_representantes:
    #         repre_id = ids

    #     qs = Representative.objects.filter(id = repre_id).values(
    #         'email'
    #     )

    #     kwargs['email'] = qs
    #     return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        messages.success(self.request, _('Apoderado Creado'))
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class RepresentativeList(View):
    """
    clase que crea el json/datos para la tabla
    """
    template_name = 'representative/representativet_list.html'

    def get(self, request, *args, **kwargs):
        representative = list(Representative.objects.values())
        data = {'representatives': []}

        for representatives in representative:
            representative_data = {
                'name': representatives['name'],
                'last_name': representatives['last_name'],
                'rut': representatives['rut'],
                'email': representatives['email'],
                'phone': representatives['phone'],
                'edit_url': reverse('representative:edit_representative', kwargs={'pk': representatives['id']}),
                'delete_url': reverse('representative:delete_representative', kwargs={'pk': representatives['id']}),
            }
            data['representatives'].append(representative_data)

        return JsonResponse(data)

class RepresentativeLists(View):
    """
    Clase que visualiza pagina de list
    """
    template_name = 'representative/representative_list.html'

    def get(self, request, *args, **kwargs):
        context = {'segment': 'index'}
        html_template = loader.get_template(self.template_name)
        return HttpResponse(html_template.render(context, request))

class RepresentativeEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Representative
    form_class = CreateRepresentativeForm
    template_name = 'representative/representative_create.html'
    success_url = reverse_lazy('representative:create_representative')

    def get_object(self, queryset=None):
        return get_object_or_404(Representative, id=self.kwargs['pk'])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        form.initial = {
            'rut': instance.rut,
            'name': instance.name,
            'last_name': instance.last_name,
            'email': instance.email,
            'email_2': instance.email,
            'phone': instance.phone,
            'password_representative': instance.password_representative,
        }
        return form
    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Apoderado Editado'))
        return HttpResponseRedirect(self.request.path)

    def form_invalid(self, form):
        print(form.errors)
        response = super().form_invalid(form)
        messages.error(self.request, _('Error al editar el Apoderado. Por favor, corrige los errores en el formulario.'))
        return response
class RepresentativeDelete(LoginRequiredMixin, DeleteView):
    model = Representative
    template_name = 'representative/confirm_delete.html'
    success_url = reverse_lazy('representative:list_representatives')  # Ajusta según tu configuración

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' not in kwargs:
            context['form'] = ConfirmDeleteForm()

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        self.object = self.get_object()
        form = ConfirmDeleteForm(request.POST, instance=self.object)

        if form.is_valid():
            #***CORRGIR ESTE MSJ, AVECES APARECE AL CREAR UN STUDENT
            #messages.success(self.request, _('Alumno Eliminado'))
            response = self.delete(request, *args, **kwargs)
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))