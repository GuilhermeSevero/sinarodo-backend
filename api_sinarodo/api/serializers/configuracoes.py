from ..models.configuracoes import Configuracoes
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from django.db import transaction
import json
import datetime
from .logs import LogsSerializer, Logs


class ConfiguracoesSerializer(FlexFieldsModelSerializer):
    id_usuario = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Configuracoes
        fields = ('acrescimo_encarregado', 'dias_em_campo', 'premio_seis', 'premio_sete', 'premio_oito', 'premio_nove',
                  'premio_dez', 'id_usuario')

    @transaction.atomic(using='default')
    def save(self, **kwargs):
        id_usuario = self.initial_data.get('id_usuario')

        config = super(ConfiguracoesSerializer, self).save(**kwargs)

        log = LogsSerializer(data={
            'id_usuario': id_usuario,
            'model': 'configuracoes',
            'tipo': Logs.INFO,
            'log': json.dumps(self.data)
        })
        log.is_valid(raise_exception=True)
        log.save()

        return config
