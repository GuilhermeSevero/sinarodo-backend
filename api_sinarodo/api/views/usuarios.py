from ..serializers.usuarios import Usuarios, UsuariosSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password


class UsuariosFilterSet(FilterSet):
    class Meta:
        model = Usuarios
        fields = ('id', 'nome', 'apelido', 'matricula', 'cpf', 'email', 'funcao_1', 'funcao_2', 'login', 'permissao')


class UsuariosView(FlexFieldsMixin, ModelViewSet):
    serializer_class = UsuariosSerializer
    queryset = Usuarios.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = UsuariosFilterSet
    search_fields = ('nome', 'apelido', 'matricula', 'cpf', 'email', )
    ordering_fields = ('id', 'nome')

    permit_list_expands = []

    @action(methods=["POST"], detail=False)
    def autenticar(self, request, *args, **kwargs):
        login = request.data.get('login', None)
        password = request.data.get('password', None)

        if login and password:
            try:
                usuario = Usuarios.objects.get(login=login)
                if check_password(password=password, encoded=usuario.password):
                    return Response(UsuariosSerializer(usuario).data)
                raise serializers.ValidationError('Senha Inválida!')
            except Usuarios.DoesNotExist:
                raise serializers.ValidationError('Login Inválido!')
        raise serializers.ValidationError('Informe os campos "login" e "password"!')
