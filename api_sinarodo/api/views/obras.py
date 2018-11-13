from ..serializers.obras import Obras, ObrasSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import DateFilter


class ObrasFilterSet(FilterSet):
    data_lancamento__gte = DateFilter(field_name='data_lancamento', lookup_expr='gte')
    data_lancamento__lte = DateFilter(field_name='data_lancamento', lookup_expr='lte')
    data_inicio__gte = DateFilter(field_name='data_inicio', lookup_expr='gte')
    data_inicio__lte = DateFilter(field_name='data_inicio', lookup_expr='lte')
    data_final__gte = DateFilter(field_name='data_final', lookup_expr='gte')
    data_final__lte = DateFilter(field_name='data_final', lookup_expr='lte')

    class Meta:
        model = Obras
        fields = ('id', 'pedido')


class ObrasView(FlexFieldsMixin, ModelViewSet):
    serializer_class = ObrasSerializer
    queryset = Obras.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ObrasFilterSet
    ordering_fields = ('id', 'pedido')

    permit_list_expands = []
