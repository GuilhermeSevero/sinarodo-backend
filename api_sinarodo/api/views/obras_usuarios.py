from ..serializers.obras_usuarios import ObrasUsuarios, ObrasUsuariosSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from django_filters import NumberFilter


class ObrasUsuariosFilterSet(FilterSet):
    id_obra = NumberFilter(field_name='obra__id')
    id_usuario = NumberFilter(field_name='usuario__id')

    class Meta:
        model = ObrasUsuarios
        fields = ('id', 'nota_final')


class ObrasUsuariosView(FlexFieldsMixin, ModelViewSet):
    serializer_class = ObrasUsuariosSerializer
    queryset = ObrasUsuarios.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ObrasUsuariosFilterSet
    ordering_fields = ('id',)

    permit_list_expands = [
        'obra',
        'usuario'
    ]
