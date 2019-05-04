from ..serializers.logs import Logs, LogsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import DateFilter, NumberFilter
from rest_framework import serializers


class LogsFilterSet(FilterSet):
    data_hora__gte = DateFilter(field_name='data_hora', lookup_expr='gte')
    data_hora__lte = DateFilter(field_name='data_hora', lookup_expr='lte')
    usuario__id = NumberFilter(field_name='usuario__id')

    class Meta:
        model = Logs
        fields = ('id', 'model', 'tipo')


class LogsView(FlexFieldsMixin, ModelViewSet):
    serializer_class = LogsSerializer
    queryset = Logs.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = LogsFilterSet
    search_fields = ('usuario__nome',)
    ordering_fields = ('id', 'data_hora', 'model')

    permit_list_expands = [
        'usuario'
    ]

    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError('Não é permitido alterar Log!')

    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError('Não é permitido excluir Log!')
