"""Fairmedias serializer."""
# serializers
from rest_framework import serializers
# models
from myhandycrafts.fairs.models  import FairMedia

class FairMediaModelSerializer(serializers.ModelSerializer):

    img_huge = serializers.ImageField(required=True)

    class Meta:
        model = FairMedia
        fields = (
            'id',
            'fair',
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
