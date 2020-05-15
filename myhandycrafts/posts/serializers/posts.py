""""Post serialisers."""

# Django REST Framework
from rest_framework import serializers

# models
from myhandycrafts.posts.models import Post

# serializer
from myhandycrafts.users.serializers import UserShortDetailSerializer
from myhandycrafts.categories.serializers import CategoryListSerializer
from .postmedias import PostMediaModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """Post Model Serializer."""
    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'category',
            'description',
            'price',
            'quantity',
            'state',
            'created_at',
            'updated_at',
        )

class PostDetailModelSerializer(serializers.ModelSerializer):
    """Post Model Serializer."""
    user = UserShortDetailSerializer(many=False)
    category = CategoryListSerializer(many=False)
    postmedias = PostMediaModelSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'category',
            'description',
            'price',
            'quantity',
            'state',
            'postmedias',
            'created_at',
            'updated_at',
        )