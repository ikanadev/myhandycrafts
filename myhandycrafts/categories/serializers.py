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
        validators=[UniqueValidator(queryset=Category.objects.filter(active=True))]
    )

    description = serializers.CharField(
        allow_blank=True,
        max_length=512,
    )

    image = serializers.ImageField(required=False)

    class Meta:
        """Meta class."""
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'image',
            'count_post',
            'count_craftman',
        )

        only_read_fields = (
            'count_post',
            'count_craftman',
        )


class CategoryListSerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        """Meta class."""
        model = Category
        fields = (
            'id',
            'name',
        )




