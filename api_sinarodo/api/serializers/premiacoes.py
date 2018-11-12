from ..models.premiacoes import Premiacoes
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .categorias import CategoriasSerializer


class PremiacoesSerializer(FlexFieldsModelSerializer):
    id_categoria = serializers.IntegerField(source='categoria_id', required=True)

    class Meta:
        model = Premiacoes
        fields = ('id', 'id_categoria', 'mes_periodo', 'ano_periodo', 'dias_em_campo', 'nota')

        expandable_fields = {
            'categoria': (CategoriasSerializer, {'source': 'categoria'})
        }
