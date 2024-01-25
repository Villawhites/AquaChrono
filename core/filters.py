import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class GenericFilter(django_filters.FilterSet):
    """
    Filtro generico para una barra
    de busqueda sobre la tabla
    Hay que definiri en view, el filter_fields = []
    y añadirlo en el método get_queryset:
    self.filterset_class.filter_fields = self.filter_fields
    """
    filter_fields=None
    search = django_filters.CharFilter(
        label=_("Buscar"),
        method="search_def"
    )

    def __init__(self, *args, **kwargs):
        super(GenericFilter, self).__init__(*args, **kwargs)
        self.filters['search'].field.widget.attrs.update({
            'class': 'form-control'
        })

    def search_def(self, queryset, name, value):
        qs = queryset
        qr = Q()
        for field in self.filter_fields:
            qr |= Q(**{f'{field}__icontains': value })
        qs = queryset.filter(qr)
        return qs