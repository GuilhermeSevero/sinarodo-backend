from ..models.logs import Logs
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .usuarios import UsuariosSerializer


class LogsSerializer(FlexFieldsModelSerializer):
    id_usuario = serializers.IntegerField(source='usuario_id', required=True)

    class Meta:
        model = Logs
        fields = ('id', 'data_hora', 'id_usuario', 'model', 'tipo', 'log')

    expandable_fields = {
        'usuario': (UsuariosSerializer, {'source': 'usuario'})
    }
