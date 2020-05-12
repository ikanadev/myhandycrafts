"""Departament serializer."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.maps.models import Departament


class DepartamentModelSerializer(serializers.ModelSerializer):
    """Departament model serializer."""
    name = serializers.CharField(min_length=2,
                                 max_length=32,
                                 validators=[UniqueValidator(
                                     queryset=Departament.objects.filter(
                                         active=True
                                     )
                                 )]
                                 )

    class Meta:
        model = Departament
        fields = (
            'id',
            'name',
            'description',
        )



class DepartamentListSerializer(serializers.ModelSerializer):
    """Departament model serializer."""

    class Meta:
        """Meta class."""
        model = Departament
        fields = (
            'id',
            'name',
        )
