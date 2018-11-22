from ..serializers.obras_usuarios import ObrasUsuarios, ObrasUsuariosSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter, CharFilter, DateFilter


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
