from ..models.usuarios import Usuarios
from rest_flex_fields import FlexFieldsModelSerializer
from django.contrib.auth.hashers import make_password


class UsuariosSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(
            password=validated_data.get('password', 12345678),
            salt=None,
            hasher='pbkdf2_sha256'
        )
        return super(UsuariosSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get('password', None) and validated_data['password'] != instance.password:
            validated_data['password'] = make_password(
                password=validated_data['password'],
                salt=None,
                hasher='pbkdf2_sha256'
            )
        return super(UsuariosSerializer, self).update(instance, validated_data)
