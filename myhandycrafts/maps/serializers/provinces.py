"""Province serializer."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.maps.models import Province

# serializer
from myhandycrafts.maps.serializers import DepartamentListSerializer






class ProvinceModelSerializer(serializers.ModelSerializer):
    """Province model serializer."""
    name = serializers.CharField(min_length=2,
                                 max_length=32,
                                 validators=[UniqueValidator(
                                     queryset=Province.objects.filter(
                                         active=True
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
        if not data.active:
            raise serializers.ValidationError("Invalid departament")
        return data


class ProvinceListSerializer(serializers.ModelSerializer):
    """Province model serializer."""

    class Meta:
        """Meta class."""
        model = Province
        fields = (
            'id',
            'name',
        )
