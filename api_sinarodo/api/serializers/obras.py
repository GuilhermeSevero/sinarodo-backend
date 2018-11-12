from ..models.obras import Obras
from rest_flex_fields import FlexFieldsModelSerializer


class ObrasSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Obras
        fields = '__all__'
