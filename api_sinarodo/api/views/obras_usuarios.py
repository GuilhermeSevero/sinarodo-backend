from ..serializers.obras_usuarios import ObrasUsuarios, ObrasUsuariosSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter, CharFilter, DateFilter, BooleanFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers


class ObrasUsuariosFilterSet(FilterSet):
    id_obra = NumberFilter(field_name='obra__id')
    id_usuario = NumberFilter(field_name='usuario__id')

    obra_pedido = NumberFilter(field_name='obra__pedido')
    obra_data_lancamento__gte = DateFilter(field_name='obra__data_lancamento', lookup_expr='gte')
    obra_data_lancamento__lte = DateFilter(field_name='obra__data_lancamento', lookup_expr='lte')
    obra_data_inicio__gte = DateFilter(field_name='obra__data_inicio', lookup_expr='gte')
    obra_data_inicio__lte = DateFilter(field_name='obra__data_inicio', lookup_expr='lte')
    obra_data_final__gte = DateFilter(field_name='obra__data_final', lookup_expr='gte')
    obra_data_final__lte = DateFilter(field_name='obra__data_final', lookup_expr='lte')

    usuario_cpf = CharFilter(field_name='usuario__cpf')
    usuario_matricula = NumberFilter(field_name='usuario__matricula')

    encarregado = BooleanFilter(field_name='encarregado')

    class Meta:
        model = ObrasUsuarios
        fields = ('id', 'encarregado')


class ObrasUsuariosView(FlexFieldsMixin, ModelViewSet):
    serializer_class = ObrasUsuariosSerializer
    queryset = ObrasUsuarios.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = ObrasUsuariosFilterSet
    search_fields = ('usuario__nome', )
    ordering_fields = ('id', 'nota_final', 'obra__pedido', 'usuario__nome')

    permit_list_expands = [
        'obra',
        'usuario'
    ]

    @action(methods=["PATCH"], detail=True)
    def diminuir_dias_em_campo(self, request, *args, **kwargs):
        mes = request.data.get('mes_periodo', None)
        ano = request.data.get('ano_periodo', None)
        dias = request.data.get('dias', None)

        if not (mes and ano and dias):
            raise serializers.ValidationError('Parametros incorretos. Informe o mes_periodo, ano_periodo e dias!')

        id_usuario_obras = kwargs.get('pk', None)

        try:
            obras_usuario = ObrasUsuarios.objects.get(pk=id_usuario_obras)
        except ObrasUsuarios.DoesNotExist:
            raise serializers.ValidationError('Registro não encontrado!')

        for premio in obras_usuario.premiacoes.all():
            premio.dias_em_campo -= dias
            premio.save()

        return Response('{dias} dias em campo diminuidos com sucesso!'.format(dias=dias))
