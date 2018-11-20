from ..serializers.premiacoes import Premiacoes, PremiacoesSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter


class PremiacoesFilterSet(FilterSet):
    id_categoria = NumberFilter(field_name='categoria__id')

    class Meta:
        model = Premiacoes
        fields = ('id', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')


class PremiacoesView(FlexFieldsMixin, ModelViewSet):
    serializer_class = PremiacoesSerializer
    queryset = Premiacoes.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PremiacoesFilterSet
    ordering_fields = ('id',)

    permit_list_expands = [
        'categoria',
        'obras_usuario'
    ]
