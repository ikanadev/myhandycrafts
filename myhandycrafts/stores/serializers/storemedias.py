"""Fairmedias serializer."""
# Django
from django.utils.translation import ugettext_lazy as _

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

    def validate_store(self,data):
        user = self.context['user']
        if not user.is_staff:
            if user != data.user:
                raise serializers.ValidationError(_('Invalid store, you are not owner'))
        return data