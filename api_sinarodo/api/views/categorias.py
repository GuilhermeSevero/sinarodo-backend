from ..serializers.categorias import Categorias, CategoriasSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin


class CategoriasFilterSet(FilterSet):
    class Meta:
        model = Categorias
        fields = ('id', 'descricao', 'peso')


class CategoriasView(FlexFieldsMixin, ModelViewSet):
    serializer_class = CategoriasSerializer
    queryset = Categorias.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = CategoriasFilterSet
    search_fields = ('descricao',)
    ordering_fields = ('id', 'descricao', 'peso')

    permit_list_expands = []
