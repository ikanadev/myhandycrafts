"""Fairmedias serializer."""
# serializers
from rest_framework import serializers
# models
from myhandycrafts.stores.models import StoreMedia

class StoreMediaModelSerializer(serializers.ModelSerializer):

    img_huge = serializers.ImageField(required=True)

    class Meta:
        model = StoreMedia
        fields = (
            'id',
            'store',
            'img_huge',
            'img_standar',
            'img_small',
            'order',
        )

        # read_only_fields = (
        #     'img_huge',
        #     'img_standar',
        #     'img_small',
        #     'order',
        # )
