"""Postmedias serializer."""
# serializers
from rest_framework import serializers
# models
from myhandycrafts.posts.models import PostMedia

class PostMediaModelSerializer(serializers.ModelSerializer):

    img_huge = serializers.ImageField(required=True)

    class Meta:
        model = PostMedia
        fields = (
            'id',
            'post',
            'img_huge',
            'img_standar',
            'img_small',
            'img_thumbnail',
            'order',
        )

        # read_only_fields = (
        #     'img_huge',
        #     'img_standar',
        #     'img_small',
        #     'order',
        # )
