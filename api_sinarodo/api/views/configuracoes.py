from ..serializers.configuracoes import Configuracoes, ConfiguracoesSerializer
from rest_framework.viewsets import ModelViewSet
from rest_flex_fields.views import FlexFieldsMixin


class CategoriasView(FlexFieldsMixin, ModelViewSet):
    serializer_class = ConfiguracoesSerializer
    queryset = Configuracoes.objects.all()
    ordering_fields = ('id',)

    permit_list_expands = []
