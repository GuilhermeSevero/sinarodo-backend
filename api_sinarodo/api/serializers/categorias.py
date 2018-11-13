from ..models.categorias import Categorias
from rest_flex_fields import FlexFieldsModelSerializer
from django.db.models import Sum
from rest_framework import serializers


class CategoriasSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'

    def validate(self, attrs):
        peso_anterior = self.instance.peso if self.instance else 0
        soma = Categorias.objects.all().aggregate(Sum('peso'))['peso__sum']
        if (soma + attrs.get('peso', 0)) - peso_anterior > 100:
            raise serializers.ValidationError('Peso total não pode ultrapassar 100%!')
        return super(CategoriasSerializer, self).validate(attrs)
