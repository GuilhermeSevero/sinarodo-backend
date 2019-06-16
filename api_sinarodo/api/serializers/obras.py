from ..models.obras import Obras
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers


class ObrasSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Obras
        fields = '__all__'

    # def validate(self, attrs):
    #     if hasattr(self.instance, 'usuarios_obra') and self.instance.usuarios_obra.all():
    #         raise serializers.ValidationError('Não é possível alterar uma Obra que já foi premiada! <br>'
    #                                           'Exclua os registros de premiação para continuar.')
    #     return super(ObrasSerializer, self).validate(attrs)
