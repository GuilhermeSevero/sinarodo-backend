from ..models.premiacoes import Premiacoes
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .categorias import CategoriasSerializer
from .obras_usuarios import ObrasUsuariosSerializer


class PremiacoesSerializer(FlexFieldsModelSerializer):
    id_categoria = serializers.IntegerField(source='categoria_id', required=True)
    id_obras_usuario = serializers.IntegerField(source='obras_usuario_id', required=True)

    class Meta:
        model = Premiacoes
        fields = ('id', 'id_categoria', 'id_obras_usuario', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')

    expandable_fields = {
        'categoria': (CategoriasSerializer, {'source': 'categoria'}),
        'obras_usuario': (ObrasUsuariosSerializer, {'source': 'obras_usuario'})
    }
