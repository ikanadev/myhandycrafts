"""Province serializer."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.maps.models import Province

# serializer
from myhandycrafts.maps.serializers import DepartamentListSerializer

#utils
from django.utils.translation import ugettext_lazy as _






class ProvinceModelSerializer(serializers.ModelSerializer):
    """Province model serializer."""
    name = serializers.CharField(min_length=2,
                                 max_length=32
                                 )

    class Meta:
        model = Province
        fields = (
            'id',
            'departament',
            'name',
            'description',
        )

    def validate_name(self,data):
        qs = Province.objects.filter(active=True)
        if self.instance is not None:
            if qs.filter(name=data).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(_("Name departament already exists"))
        else:
            if qs.filter(name=data).exists():
                raise serializers.ValidationError(_("Name departament already exists"))
        return data

    def validate_departament(self,data):
        """validate valid departament"""
        if not data.active:
            raise serializers.ValidationError("Invalid departament")
        return data

class ProvinceDetailModelSerializer(serializers.ModelSerializer):
    """Province model serializer."""

    departament=DepartamentListSerializer(many=False)

    class Meta:
        model = Province
        fields = (
            'id',
            'departament',
            'name',
            'description',
        )

class ProvinceListSerializer(serializers.ModelSerializer):
    """Province model serializer."""

    class Meta:
        """Meta class."""
        model = Province
        fields = (
            'id',
            'name',
        )
