from ..models.obras_usuarios import ObrasUsuarios
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .obras import ObrasSerializer
from .usuarios import UsuariosSerializer


class ObrasUsuariosSerializer(FlexFieldsModelSerializer):
    id_obra = serializers.IntegerField(source='obra_id', required=True)
    id_usuario = serializers.IntegerField(source='usuario_id', required=True)

    class Meta:
        model = ObrasUsuarios
        fields = ('id', 'id_obra', 'id_usuario', 'nota_final', 'observacao', 'encarregado', 'periodos')

    expandable_fields = {
        'obra': (ObrasSerializer, {'source': 'obra'}),
        'usuario': (UsuariosSerializer, {'source': 'usuario'})
    }

    # def validate(self, attrs):
    #     try:
    #         obras_usuario = ObrasUsuarios.objects.get(obra__id=attrs.get('obra_id'), usuario__id=attrs.get('usuario_id'))
    #
    #         raise serializers.ValidationError('Usuário {nome} já foi premiado por essa obra!'
    #                                           .format(nome=obras_usuario.usuario.nome))
    #     except ObrasUsuarios.DoesNotExist:
    #         return super(ObrasUsuariosSerializer, self).validate(attrs)
