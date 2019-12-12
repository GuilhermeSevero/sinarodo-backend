from ..serializers.obras import Obras, ObrasSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import DateFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from ..utils.premiacao import Premiacao
from rest_framework import serializers


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
    ordering_fields = (
        'id',
        'pedido',
        'data_lancamento',
        'data_inicio',
        'data_final'
    )

    permit_list_expands = []

    @action(methods=['POST'], detail=False)
    @transaction.atomic(using='default')
    def premiacao(self, request, *args, **kwargs):
        usuarios = request.data.get('usuarios', [])
        categorias = request.data.get('categorias', [])
        id_obra = request.data.get('id_obra', None)
        premiacao_observacao = request.data.get('premiacao_observacao', '')
        encarregado = request.data.get('encarregado', False)
        data_inicio = request.data.get('data_inicio', None)
        data_final = request.data.get('data_final', None)

        if not (usuarios and categorias and id_obra and data_inicio and data_final):
            raise serializers.ValidationError('Parâmetros incorretos!')

        if encarregado and not usuarios.__contains__(encarregado):
            usuarios.append(encarregado)

        premiacao = Premiacao(
            id_obra=id_obra,
            categorias=categorias,
            data_incio=data_inicio,
            data_final=data_final,
            observacao=premiacao_observacao
        )

        for id_usuario in usuarios:
            premiacao.premiar(id_usuario=id_usuario, encarregado=(encarregado and encarregado == id_usuario))

        return Response('Premiação realizada com sucesso!')

    @staticmethod
    def _criar_obra(dados):
        obra = ObrasSerializer(
            data={
                **dados
            }
        )
        obra.is_valid(raise_exception=True)
        obra.save()
        return obra.instance
