"""Province serializer."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.maps.models import Province


class ProvinceModelSerializer(serializers.ModelSerializer):
    """Province model serializer."""
    name = serializers.CharField(min_length=2,
                                 max_length=32,
                                 validators=[UniqueValidator(
                                     queryset=Province.objects.filter(
                                         is_deleted=False
                                     )
                                 )]
                                 )

    class Meta:
        model = Province
        fields = (
            'id',
            'departament',
            'name',
            'description',
        )

    def validate_departament(self,data):
        """validate valid departament"""
        if data.is_deleted:
            raise serializers.ValidationError("Invalid departament")
        return data

