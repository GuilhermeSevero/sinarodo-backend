from ..serializers.premiacoes import Premiacoes, PremiacoesSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter


class PremiacoesFilterSet(FilterSet):
    id_categoria = NumberFilter(field_name='categoria__id')
    pedido = NumberFilter(field_name='obras_usuario__obra__pedido')
    id_usuario_obra = NumberFilter(field_name='obras_usuario__id')

    class Meta:
        model = Premiacoes
        fields = ('id', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')


class PremiacoesView(FlexFieldsMixin, ModelViewSet):
    serializer_class = PremiacoesSerializer
    queryset = Premiacoes.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PremiacoesFilterSet
    ordering_fields = (
        'id',
        'ano_periodo',
        'mes_periodo',
        'obras_usuario__usuario__nome',
        'categoria__descricao'
    )

    permit_list_expands = [
        'categoria',
        'obras_usuario',
        'obras_usuario.obra',
        'obras_usuario.usuario'
    ]
