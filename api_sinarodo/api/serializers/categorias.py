from ..models.categorias import Categorias
from rest_flex_fields import FlexFieldsModelSerializer


class CategoriasSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'
