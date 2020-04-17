""" Categories serializers."""

# Django

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.categories.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    """Category model serializer."""

    name = serializers.CharField(
        min_length=4,
        max_length=128,
        validators=[UniqueValidator(queryset=Category.objects.filter(is_deleted=False))]
    )

    description = serializers.CharField(
        allow_blank=True,
        max_length=512,
    )

    class Meta:
        """Meta class."""
        model = Category
        fields = (
            'id',
            'name',
            'description',
        )





