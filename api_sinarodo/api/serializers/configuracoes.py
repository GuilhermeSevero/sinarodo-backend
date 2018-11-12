from ..models.configuracoes import Configuracoes
from rest_flex_fields import FlexFieldsModelSerializer


class ConfiguracoesSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Configuracoes
        fields = '__all__'
