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

from .models import Student
from .form import ConfirmDeleteForm, CreateStundentForm


# Create your views here.
class StudentCreate(CreateView):
    model = Student
    form_class = CreateStundentForm
    template_name = 'student/student_create.html'
    success_url = reverse_lazy('student:create_student')

    def form_valid(self, form):
        try:
            obj = form.save(commit=False)
            obj.save()
            messages.success(self.request, _('Alumno Creado'))
            return super().form_valid(form)
        except IntegrityError:
            form.add_error("id", 'El codigo ya existe')
            messages.error(self.request, _('Hubo un problema al crear al alumno.'))
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class StudentList(View):
    """
    clase que crea el json/datos para la tabla
    """
    template_name = 'student/student_list.html'

    def get(self, request, *args, **kwargs):
        students = list(Student.objects.values())
        data = {'students': []}

        for student in students:
            student_data = {
                'name': student['name'],
                'rut': student['rut'],
                'birth_date': student['birth_date'],
                'edit_url': reverse('student:edit_student', kwargs={'pk': student['id']}),
                'delete_url': reverse('student:delete_student', kwargs={'pk': student['id']}),
            }
            data['students'].append(student_data)

        return JsonResponse(data)

class StudentLists(View):
    """
    Clase que visualiza pagina de list
    """
    template_name = 'student/student_list.html'

    def get(self, request, *args, **kwargs):
        context = {'segment': 'index'}
        html_template = loader.get_template(self.template_name)
        return HttpResponse(html_template.render(context, request))


class StudentEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = CreateStundentForm
    template_name = 'student/student_create.html'
    success_url = reverse_lazy('student:create_student')

    def get_object(self, queryset=None):
        return get_object_or_404(Student, id=self.kwargs['pk'])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        instance = self.get_object()
        form.initial = {
            'rut': instance.rut,
            'name': instance.name,
            'birth_date': instance.birth_date,
        }
        return form

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Alumno Editado'))
        return HttpResponseRedirect(self.request.path)

    def form_invalid(self, form):
        print(form.errors)
        response = super().form_invalid(form)
        messages.error(self.request, _('Error al editar el alumno. Por favor, corrige los errores en el formulario.'))
        return response

class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student/confirm_delete.html'
    success_url = reverse_lazy('student:list_students')  # Ajusta según tu configuración

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
