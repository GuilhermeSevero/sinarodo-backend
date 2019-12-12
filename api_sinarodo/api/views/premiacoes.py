from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter, BooleanFilter
from rest_framework import serializers
from rest_framework.response import Response
from ..serializers.premiacoes import Premiacoes, PremiacoesSerializer


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

    @action(methods=['GET'], detail=False)
    def relatorio_mensal(self, request, *args, **kwargs):
        mes = request.query_params.get('mes', None)
        ano = request.query_params.get('ano', None)

        if not (mes and ano):
            raise serializers.ValidationError('Informe o Mês e o Ano para o relatório!')

        return Response(self.get_serializer().buscar_dados_mensais(mes=mes, ano=ano))

    @action(methods=['GET'], detail=False)
    def relatorio_anual(self, request, *args, **kwargs):
        ano = request.query_params.get('ano', None)

        if not ano:
            raise serializers.ValidationError('Informe o Ano para o relatório!')

        return Response(self.get_serializer().buscar_dados_anual(ano=ano))

    @action(methods=['GET'], detail=False)
    def relatorio_usuario(self, request, *args, **kwargs):
        mes = request.query_params.get('mes', None)
        ano = request.query_params.get('ano', None)
        usuario = request.query_params.get('usuario', None)

        if not (usuario and mes and ano):
            raise serializers.ValidationError('Informe o Usuário, Mês e o Ano para o relatório!')

        return Response(self.get_serializer().buscar_dados_usuario(mes=mes, ano=ano, usuario=usuario))
